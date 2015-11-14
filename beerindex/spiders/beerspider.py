from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
from beerindex.items import BeerindexItem
import logging
import lxml.html
from urlparse import urlparse
import re

class BeerSpider(Spider):
    name = "beerspider"

    beer_sites = {
        'www.wbeer.com.br':
        {
            "start_url" : 'https://www.wbeer.com.br/browse.ep?cID=103354',
            "next_link" : '.paginacao li.prox a::attr(href)',
            "product_link" : '.catalogo-lista .lista .informacoes a::attr("href")',
            "xpath_title" : "//span[@itemprop='name']//text()",
            "xpath_price" : "//div[@class='preco-por']//text()",
            "xpath_style" : "//div[@class='resumo']//span[@class='nome-tipo']//text()"
        },
        'www.emporioveredas.com.br' : {
            "start_url" : 'http://www.emporioveredas.com.br/cervejas-importadas.html',
            "next_link" : '.pager a.next::attr(href)',
            "product_link" : '.products-grid a.product-image ::attr("href")',
            "xpath_title" : "//h1[@itemprop='name']//text()",
            "xpath_price" : "//div[@class='product-shop']//span[@itemprop='price']//text()",
            "xpath_style" : "//table[@id='product-attribute-specs-table']//tr[contains(.,'Estilo')]//td[last()]//text()"
        },
        'www.mundodascervejas.com' : {
            "start_url" : 'http://www.mundodascervejas.com/buscar?q=cerveja',
            "next_link" : '.topo .pagination a[rel="next"]::attr("href")',
            "product_link" : '#listagemProdutos a.produto-sobrepor::attr("href")',
            "xpath_title" : "//h1[@itemprop='name']//text()",
            "xpath_price" : "//div[@class='principal']//div[contains(@class,'preco-produto')]//strong[contains(@class,'preco-promocional')]//text()",
            "xpath_style" : "//div[@id='descricao']//table//tr[contains(.,'Estilo')]//td[last()]//text()"
        },
        'www.clubeer.com.br': {
            "start_url" : 'http://www.clubeer.com.br/loja',
            "next_link" : '#pagination li.current + li a::attr("href")',
            "product_link" : '.minhascervejas li .areaborder > a:first-child::attr("href")',
            "xpath_title" : "//h1[@itemprop='name']//text()",
            "xpath_price" : "//div[@id='principal']//div[contains(@class,'areaprecos')]//span[@itemprop='price']//text()",
            "xpath_style" : "//div[contains(@class,'areaprodutoinfoscontent')]//ul[contains(.,'ESTILO')]//li[position()=2]//text()"
        },
        'www.clubedomalte.com.br': {
            "start_url" : 'http://www.clubedomalte.com.br/pais',
            "next_link" : '.paginacao li.pg:last-child a::attr("href")',
            "product_link" : '.mainBar .spotContent > a:first-child::attr("href")',
            "xpath_title" : "//h1[@itemprop='name']//text()",
            "xpath_price" : "//div[contains(@class,'interna')]//div[contains(@class,'preco')]//*[@itemprop='price']//text()",
            "xpath_style" : "//div[contains(@class,'areaprodutoinfoscontent')]//ul[contains(.,'ESTILO')]//li[position()=2]//text()"
        }

    }

    def domain_from_url(self,url):
        parsed = urlparse(url)
        return parsed.netloc

    #allowed_domains = ["www.cervejastore.com.br"]
    # start_urls = ['http://www.mundodascervejas.com/buscar?q=cerveja']
    # start_urls = ["http://www.emporioveredas.com.br/cervejas-importadas.html"]
    start_urls = [beer_sites[store]["start_url"] for store in beer_sites]

    def parse(self,response):
        domain = self.domain_from_url(response.url)
        for url in response.css(self.beer_sites[domain]["next_link"]).extract():
            request = Request(response.urljoin(url.strip()), self.parse)
            yield request

        titles = response.css(self.beer_sites[domain]["product_link"]).extract()
        for title in titles:
            yield Request(response.urljoin(title), self.parse_product)


    def parse_product(self,response):
        domain = self.domain_from_url(response.url)
        item = BeerindexItem()
        item["name"] = response.xpath(self.beer_sites[domain]["xpath_title"]).extract_first()
        item["style"] = response.xpath(self.beer_sites[domain]["xpath_style"]).extract_first()
        item["link"] = response.url
        item["price"] = "".join(response.xpath(self.beer_sites[domain]["xpath_price"]).extract())
        item["price"] = re.sub(r"\s+", "", item["price"], flags=re.UNICODE)
        item["price"] = re.sub(r"[^\d,\.+]", "", item["price"], flags=re.UNICODE)
        item["price"] = re.sub(r",", ".", item["price"], flags=re.UNICODE)
        yield item
