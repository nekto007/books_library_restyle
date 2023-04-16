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

5. Download by category

You can use the following arguments when running the file - parse_tululu_category.py:
All of the above arguments are optional.

    --start_page - the number of the page from which the program will start the download. Type is int(integer). The default is 1.
    --end_page - the number of the page up to which the program is downloading (not including it). Type is int(integer). The default is 2.
    --dest_folder - path to working directory of the script. This is the directory where the program will save the result of its work: books and pictures to them in the corresponding directories books, img, as well as data in json format. The type is string(string). By default, the working directory is the directory where the script parse_tululu_category.py is located.
    --skip_txt - if you run the script with this argument (you do not need to specify additional values), the program will not download images of book covers. By default, the download is enabled.
    --skip_imgs - if you run the script with this argument (no need to specify additional values) the program does not download text files of books. By default downloading is enabled.
    --json_path - path to json file, which will contain parsing results data. It is not necessary to specify the .json file extension, the script will add it automatically. Type - string(string). By default, the file will be saved in the directory with the script or (if specified) in the directory specified in the command --dest_folder. The default file name is books.json.

An example to start downloading pages 100 to 200 (inclusive):

python parse_tululu_category.py --start_page 100 --end_page 200

### Purpose of the project

The code is written for educational purposes on an online course for web developers [dvmn.org](https://dvmn.org/).