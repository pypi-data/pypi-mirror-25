# Bamboo Crawler

[![CircleCI Status](https://circleci.com/gh/kitsuyui/bamboo-crawler.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/kitsuyui/bamboo-crawler)

A Hobby Crawler.
It is almost under construction.

# Usage

## Installatino

```console
$ pip install bamboo-crawler
```

## Run

```
$ bamboo --recipe recipe.yml
```

## Recipe

```YAML
mytask:
  input:
    type: ConstantInputter
    options:
      value: http://httpbin.org/robots.txt
  process:
    type: HTTPCrawler
  output:
    type: StdoutOutputter
```

# License

BSD 2-clause "Simplified" License
