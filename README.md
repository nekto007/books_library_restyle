# Parser of books from tululu.org

A program for downloading books.

## Launch
1. Clone project
```bash 
git clone https://github.com/nekto007/books_library_restyle.git
cd books_library_restyle
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Run

From the project folder, at the command line, type `python main.py <--start_page> <--end_page>`

3.1. Example usage:

```
python main.py 30 50
```

The program will start downloading books from pages 30 to 50

4. Arguments

`--start_page` - the first page where the download will start

`--end_page` - last page where the download ends

### Purpose of the project

The code is written for educational purposes on an online course for web developers [dvmn.org](https://dvmn.org/).