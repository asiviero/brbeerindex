# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
from beerindex.items import WineIndexItem
import logging
import lxml.html
from urlparse import urlparse
import re

class WineSpider(Spider):
    name = "winespider"

    beer_sites = {
        'www.wine.com.br':
        {
            "start_url" : 'https://www.wine.com.br/browse.ep?cID=100851',
            "next_link" : '.navegacaoListagem li.prox a::attr(href)',
            "product_link" : '#listagemProdutos ul li a[itemprop="name url"]::attr("href")',
            "xpath_name" : "//h1[@itemprop='name']//text()",
            "xpath_winetype" : "//div[@class='tipoVinho']//p/text()",
            "xpath_volume" : "//div[@class='dadosAvancados']//*[@itemprop='weight']/*[@itemprop='value']/text()",
            "xpath_grape" : "//div[@class='dadosAvancados']//li[contains(.,'Uva')]//*[contains(@class,'valor')]/text()",
            "xpath_alcohol" : u"//div[@class='dadosAvancados']//li[contains(.,'Teor Alcoólico')]//*[contains(@class,'valor')]/text()",
            "xpath_country" : "//div[@id='boxProduto']//div[@class='imgPais']/p//text()",
            "xpath_region" : u"//div[@class='dadosAvancados']//li[contains(.,'Região')]//*[contains(@class,'valor')]/text()",
            "xpath_winery" : u"//div[@class='dadosAvancados']//li[contains(.,'Vinícola')]//*[contains(@class,'valor')]/text()",
            "xpath_price" : "//div[@id='boxProduto']//div[@class='boxPreco']//*[@itemprop='price']//text()",
        },
        'www.grandcru.com.br':
        {
            "start_url" : 'http://www.grandcru.com.br/vinhos.html',
            "next_link" : '.pages li a.next::attr(href)',
            "product_link" : '.products-list h2.product-name a::attr("href")',
            "xpath_name" : "//h1[@class='product-name']//text()",
            "xpath_winetype" : "//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'Tipo de Vinho')]/td/text()",
            "xpath_volume" : "//div[@class='dadosAvancados']//*[@itemprop='weight']/*[@itemprop='value']/text()",
            "xpath_grape" : "//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'Uva')]/td/text()",
            "xpath_alcohol" : u"//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'Graduação Alcoólica')]/td/text()",
            "xpath_country" : u"//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'País')]/td/text()",
            "xpath_region" : u"//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'Região Produtora')]/td/text()",
            "xpath_winery" : u"//table[contains(@class,'tbl-caracteristicas')]//tr[contains(.,'Produtor')]/td/text()",
            "xpath_price" : "//div[@class='produto_dados']//div[@class='price-box']//*[@itemprop='price']//text()",
        },
        'www.sommeliervinhos.com.br' :
        {
            "start_url" : 'http://www.sommeliervinhos.com.br/galeria.php?categoria=2',
            "next_link" : '.paginacao a.bt-proxima::attr(href)',
            "product_link" : '.lista-produtos li a::attr("href")',
            "xpath_name" : "//h1[@class='tit-paginas-h1']//text()",
            "xpath_winetype" : "//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Tipo')]/text()",
            "xpath_volume" : "//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Volume')]/text()",
            "xpath_grape" : "//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Uva')]/text()",
            "xpath_alcohol" : u"//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Alcool')]/text()",
            "xpath_country" : u"//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'País')]/text()",
            "xpath_region" : u"//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Região')]/text()",
            "xpath_winery" : u"//div[contains(@class,'prod-caracteristicas')]//li[contains(.,'Produtor')]/text()",
            "xpath_price" : "//div[@id='principal']//div[@class='valores-produtos']//*[@class='preco-atual']//text()",
        },
        'www.vinomundi.com.br':
        {
            "start_url" : 'http://www.vinomundi.com.br/vinhos',
            "next_link" : '.pages li a.next::attr(href)',
            "product_link" : 'ul.products-grid li.item h2 a::attr("href")',
            "xpath_name" : "//*[@class='product-shop']//h1//text()",
            "xpath_winetype" : "//table[contains(@class,'data-table')]//tr[contains(.,'Tipo')]/td/text()",
            "xpath_volume" : "//table[contains(@class,'data-table')]//tr[contains(.,'Volume')]/td/text()",
            "xpath_grape" : "//table[contains(@class,'data-table')]//tr[contains(.,'Uva')]/td/text()",
            "xpath_alcohol" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Alcool')]/td/text()",
            "xpath_country" : u"//table[contains(@class,'data-table')]//tr[contains(.,'País')]/td/text()",
            "xpath_region" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Região')]/td/text()",
            "xpath_winery" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Produtor')]/td/text()",
            "xpath_price" : "//div[@class='product-shop']//div[@class='price-box']//*[@class='preco-produto-valor']//@value",
        },
        # 'www.vinhosweb.com.br':
        # {
        #     "start_url" : 'http://www.vinhosweb.com.br/vinhos/vinhos',
        #     "next_link" : '.pages li a.next::attr(href)',
        #     "product_link" : 'ul.products-grid li.item h2 a::attr("href")',
        #     "xpath_name" : "//*[@class='product-shop']//h1//text()",
        #     "xpath_winetype" : "//table[contains(@class,'data-table')]//tr[contains(.,'Tipo')]/td/text()",
        #     "xpath_volume" : "//table[contains(@class,'data-table')]//tr[contains(.,'Volume')]/td/text()",
        #     "xpath_grape" : "//table[contains(@class,'data-table')]//tr[contains(.,'Uva')]/td/text()",
        #     "xpath_alcohol" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Alcool')]/td/text()",
        #     "xpath_country" : u"//table[contains(@class,'data-table')]//tr[contains(.,'País')]/td/text()",
        #     "xpath_region" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Região')]/td/text()",
        #     "xpath_winery" : u"//table[contains(@class,'data-table')]//tr[contains(.,'Produtor')]/td/text()",
        #     "xpath_price" : "//div[@class='product-shop']//div[@class='price-box']//*[@class='preco-produto-valor']//@value",
        # }
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

        item = WineIndexItem()
        item["name"] = response.xpath(self.beer_sites[domain]["xpath_name"]).extract_first().strip("\t\n\r")
        item["winetype"] = response.xpath(self.beer_sites[domain]["xpath_winetype"]).extract_first().strip("\t\n\r")
        try:
            item["volume"] = response.xpath(self.beer_sites[domain]["xpath_volume"]).extract_first().strip("\t\n\r")
        except AttributeError:
            pass
        try:
            item["grape"] = response.xpath(self.beer_sites[domain]["xpath_grape"]).extract_first().strip("\t\n\r")
        except AttributeError:
            pass
        try:
            item["alcohol"] = response.xpath(self.beer_sites[domain]["xpath_alcohol"]).extract_first()
        except AttributeError:
            pass
        item["country"] = response.xpath(self.beer_sites[domain]["xpath_country"]).extract_first().strip("\t\n\r")
        item["region"] = response.xpath(self.beer_sites[domain]["xpath_region"]).extract_first()
        item["winery"] = response.xpath(self.beer_sites[domain]["xpath_winery"]).extract_first()

        item["link"] = response.url
        item["price"] = "".join(response.xpath(self.beer_sites[domain]["xpath_price"]).extract())
        item["price"] = re.sub(r"\s+", "", item["price"], flags=re.UNICODE)
        item["price"] = re.sub(r"[^\d,\.]*", "", item["price"], flags=re.UNICODE)
        item["price"] = re.sub(r",", ".", item["price"], flags=re.UNICODE)
        yield item
