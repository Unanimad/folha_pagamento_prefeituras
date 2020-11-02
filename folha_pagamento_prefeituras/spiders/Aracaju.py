import scrapy

from folha_pagamento_prefeituras.items import PrefeituraAracajuItem


class Aracaju(scrapy.Spider):
    name = 'Aracaju'
    start_urls = ['https://transparencia.aracaju.se.gov.br/prefeitura/pessoal-2/']

    def parse(self, response, **kwargs):
        links = response.css('div#elementor-tab-content-2421 p a::attr(href)')
        for link in links:
            if '/folha/' in link.get():
                continue

            yield scrapy.Request(link.get(), callback=self.parse_anos)
            break

    def parse_anos(self, response, **kwargs):
        links = response.css('div.wp-block-column p a::attr(href)')
        for link in links:
            yield scrapy.Request(link.get(), callback=self.parse_meses)

    def parse_meses(self, response, **kwargs):
        empresas = response.css('div.w3eden h3.media-heading a::text').get()
        folhas = response.css('a.wpdm-download-link').get()
        yield PrefeituraAracajuItem(empresa=empresas, folha=folhas)
