# Dictionary Crawler ![](https://img.shields.io/apm/l/vim-mode.svg) 

This is an **open-source** crawler project which is written in python3 and [scrapy][1]. 
The main purpose of this project is to crawler all relevant information about a word. 
Therefore, you can use this package to obtain all information that you need and building your own card memory.     

### Setup

```shell script
pip install -r requirments.txt
```

### How to run a spider

```shell script
cd dictionary_crwalers
scrapy crawl longman
```

### Commands

```shell script
pip install scrapy
scrapy startproject dictionary_crwalers
cd dictionary_crwalers
scrapy crawl longman -a word=market
# scrapy crawl longman
```


### Contributors

- **Mohammad Masoumi** (Owner)


[1]: https://docs.scrapy.org/en/latest/intro/tutorial.html


