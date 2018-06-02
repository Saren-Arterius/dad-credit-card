# dad-credit-card
Automatically helps your dad to pay his credit card (Bank of China) bill. Captcha breaking function included.

# Requirements ([] = optional, for OCR training) 
OS
- python3
- cython
- chrom{e, ium}
- [tkinter]

Python libs
- numpy
- scipy
- Pillow (PIL)
- selenium
- [pyquery]

# Usage
1. `$ python3 setup.py build_ext --inplace` for once
2. `$ BOC_USERNAME=xxxx BOC_PASSWORD=yyyy WIDTHDRAW_ACCT=zzzz CHROME_UI_SCALE=1 python3 main.py`
where zzzz is internal acct number, use inspector on select acct page on your main acct`

