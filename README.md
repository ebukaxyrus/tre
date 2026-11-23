# CSV Summary Explorer and Finger Detection

Contains a Streamlit CSV profiling application and a separate local webcam finger-counting script.

## Technology stack
- Python
- Streamlit
- Pandas
- OpenCV
- MediaPipe

## Confirmed functionality
- Streamlit application reports data shape, memory, schema, nulls, previews and summary statistics
- separate aifinger.py counts fingers and labels odd/even using hand landmarks.

## Repository entry point

- `streamlit_app.py`: primary inspected Streamlit application.
- `aifinger.py`: separate local webcam finger-counting program.

## Run locally

```bash
git clone https://github.com/ebukaxyrus/tre.git
cd tre
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

To run the separate finger-counting experiment, install OpenCV and MediaPipe, connect a webcam and run `python aifinger.py` locally.

## Limitations and responsible use

The finger counter is a separate Python webcam application, not part of the Streamlit CSV page.

## Documentation and quality checklist

- [ ] Verify clean-environment installation.
- [ ] Add authentic screenshots and demonstration links.
- [ ] Add input/error-handling tests.
- [ ] Check data provenance, licensing and accessibility.

## Author

**Dimakunne Chukwuebuka Francis** · [GitHub](https://github.com/ebukaxyrus) · [Portfolio](https://xyrusportfolio.netlify.app/) · [XY AI Solution](https://xyaisolution.online/)

*Source-reviewed documentation. End-to-end deployment has not been independently verified.*
