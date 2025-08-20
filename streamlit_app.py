import streamlit as st
import pandas as pd


def format_bytes(num_bytes: int) -> str:
	"""Return a human-friendly string for a byte count."""
	for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
		if num_bytes < 1024 or unit == "TiB":
			return f"{num_bytes:.2f} {unit}"
		num_bytes /= 1024


st.set_page_config(page_title="CSV Summary Explorer", layout="wide")
st.title("CSV Summary Explorer")
st.caption("Upload a CSV file to see quick summary statistics and data quality info.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"]) 

if uploaded_file is None:
	st.info("Upload a CSV to get started.")
else:
	# Try reading the CSV with sensible defaults
	read_csv_kwargs = dict(low_memory=False)
	try:
		df = pd.read_csv(uploaded_file, **read_csv_kwargs)
	except UnicodeDecodeError:
		# Fallback for non-UTF encodings
		uploaded_file.seek(0)
		df = pd.read_csv(uploaded_file, encoding_errors="ignore", **read_csv_kwargs)
	except Exception as exc:  # noqa: BLE001
		st.error(f"Could not read the CSV: {exc}")
		st.stop()

	# Overview metrics
	st.subheader("Overview")
	col1, col2, col3 = st.columns(3)
	with col1:
		st.metric("Rows", f"{len(df):,}")
	with col2:
		st.metric("Columns", f"{df.shape[1]:,}")
	with col3:
		mem_bytes = int(df.memory_usage(deep=True).sum())
		st.metric("Memory", format_bytes(mem_bytes))

	# Preview
	st.subheader("Preview")
	rows_to_show = st.slider("Rows to preview", min_value=5, max_value=min(1000, max(5, len(df))), value=min(50, len(df)))
	st.dataframe(df.head(rows_to_show), use_container_width=True)

	# Data types and missingness
	st.subheader("Schema & Missing Values")
	missing_counts = df.isna().sum()
	missing_pct = (missing_counts / len(df)).fillna(0) * 100 if len(df) else missing_counts * 0
	schema_df = pd.DataFrame(
		{
			"column": df.columns,
			"dtype": df.dtypes.astype(str).values,
			"missing": missing_counts.values,
			"missing_%": missing_pct.round(2).values,
		}
	)
	st.dataframe(schema_df.sort_values(["missing_%", "column"], ascending=[False, True]), use_container_width=True)

	# Summary statistics
	st.subheader("Summary Statistics")
	cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
	num_summary = df.describe(include=["number"]).T
	if not num_summary.empty:
		st.markdown("**Numeric columns**")
		st.dataframe(num_summary, use_container_width=True)
	else:
		st.info("No numeric columns detected.")

	if len(cat_cols) > 0:
		st.markdown("**Categorical columns**")
		cat_summary = df[cat_cols].describe().T
		st.dataframe(cat_summary, use_container_width=True)
	else:
		st.info("No categorical columns detected.")

	# Top values per categorical column
	if len(cat_cols) > 0:
		st.subheader("Top values (categorical)")
		max_columns = 3
		columns = st.columns(min(max_columns, len(cat_cols)))
		for idx, col_name in enumerate(cat_cols):
			with columns[idx % max_columns]:
				st.markdown(f"**{col_name}**")
				vc = df[col_name].value_counts(dropna=False).head(10)
				vc_df = vc.reset_index()
				vc_df.columns = [col_name, "count"]
				st.dataframe(vc_df, use_container_width=True)