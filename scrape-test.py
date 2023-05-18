import unittest

from bs4 import BeautifulSoup

from scrape import parse_currency_info, parse_currency_infos


class MyTestCase(unittest.TestCase):
    def test_parse_currency_infos(self):
        html_raw = '''
        <a style="float:right" target="_blank" href="/statistics/rates/ratesdaily/?p=true&amp;Date=2023-05-05&amp;Type=Day"><i class="fa fa-print"></i> Версия для печати</a>
        <span style="display:none" id="tekDateCtrl">05.05.2023</span>
        <table class="currencyTable">
            <thead>
                <tr>
                    <th>Наименование иностранной валюты</th>
                    <th>Количество единиц иностранной валюты, буквенный код валюты</th>
                    <th>Официальный курс</th>
                </tr>
            </thead>
            <tbody>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-au"></i>
                                    <span class="text">Австралийский доллар</span>
                            </div>
                        </td>
                        <td class="curAmount">1 AUD</td>
                        <td class="curCours">
                            <div style="text-align:right">1,9249</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-am"></i>
                                    <span class="text">Армянский драм</span>
                            </div>
                        </td>
                        <td class="curAmount">1000 AMD</td>
                        <td class="curCours">
                            <div style="text-align:right">7,4559</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-bg"></i>
                                    <span class="text">Болгарский лев</span>
                            </div>
                        </td>
                        <td class="curAmount">1 BGN</td>
                        <td class="curCours">
                            <div style="text-align:right">1,6304</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-br"></i>
                                    <span class="text">Бразильский реал</span>
                            </div>
                        </td>
                        <td class="curAmount">10 BRL</td>
                        <td class="curCours">
                            <div style="text-align:right">5,7774</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ua"></i>
                                    <span class="text">Гривна</span>
                            </div>
                        </td>
                        <td class="curAmount">100 UAH</td>
                        <td class="curCours">
                            <div style="text-align:right">7,8128</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-dk"></i>
                                    <span class="text">Датская крона</span>
                            </div>
                        </td>
                        <td class="curAmount">10 DKK</td>
                        <td class="curCours">
                            <div style="text-align:right">4,2794</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ae"></i>
                                    <span class="text">Дирхам ОАЭ</span>
                            </div>
                        </td>
                        <td class="curAmount">10 AED</td>
                        <td class="curCours">
                            <div style="text-align:right">7,8569</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-us"></i>
                                    <span class="text">Доллар США</span>
                            </div>
                        </td>
                        <td class="curAmount">1 USD</td>
                        <td class="curCours">
                            <div style="text-align:right">2,8853</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-vn"></i>
                                    <span class="text">Донг</span>
                            </div>
                        </td>
                        <td class="curAmount">100000 VND</td>
                        <td class="curCours">
                            <div style="text-align:right">12,3054</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-eu"></i>
                                    <span class="text">Евро</span>
                            </div>
                        </td>
                        <td class="curAmount">1 EUR</td>
                        <td class="curCours">
                            <div style="text-align:right">3,1887</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-pl"></i>
                                    <span class="text">Злотый</span>
                            </div>
                        </td>
                        <td class="curAmount">10 PLN</td>
                        <td class="curCours">
                            <div style="text-align:right">6,9545</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-jp"></i>
                                    <span class="text">Иена</span>
                            </div>
                        </td>
                        <td class="curAmount">100 JPY</td>
                        <td class="curCours">
                            <div style="text-align:right">2,1435</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-in"></i>
                                    <span class="text">Индийская рупия</span>
                            </div>
                        </td>
                        <td class="curAmount">100 INR</td>
                        <td class="curCours">
                            <div style="text-align:right">3,5273</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ir"></i>
                                    <span class="text">Иранский риал</span>
                            </div>
                        </td>
                        <td class="curAmount">100000 IRR</td>
                        <td class="curCours">
                            <div style="text-align:right">6,8694</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-is"></i>
                                    <span class="text">Исландская крона</span>
                            </div>
                        </td>
                        <td class="curAmount">100 ISK</td>
                        <td class="curCours">
                            <div style="text-align:right">2,1245</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ca"></i>
                                    <span class="text">Канадский доллар</span>
                            </div>
                        </td>
                        <td class="curAmount">1 CAD</td>
                        <td class="curCours">
                            <div style="text-align:right">2,1201</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-cn"></i>
                                    <span class="text">Китайский юань</span>
                            </div>
                        </td>
                        <td class="curAmount">10 CNY</td>
                        <td class="curCours">
                            <div style="text-align:right">4,1657</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-kw"></i>
                                    <span class="text">Кувейтский динар</span>
                            </div>
                        </td>
                        <td class="curAmount">1 KWD</td>
                        <td class="curCours">
                            <div style="text-align:right">9,4198</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-md"></i>
                                    <span class="text">Молдавский лей</span>
                            </div>
                        </td>
                        <td class="curAmount">10 MDL</td>
                        <td class="curCours">
                            <div style="text-align:right">1,6142</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-nz"></i>
                                    <span class="text">Новозеландский доллар</span>
                            </div>
                        </td>
                        <td class="curAmount">1 NZD</td>
                        <td class="curCours">
                            <div style="text-align:right">1,8020</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-no"></i>
                                    <span class="text">Норвежская крона</span>
                            </div>
                        </td>
                        <td class="curAmount">10 NOK</td>
                        <td class="curCours">
                            <div style="text-align:right">2,6974</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ru"></i>
                                    <span class="text">Российский рубль</span>
                            </div>
                        </td>
                        <td class="curAmount">100 RUB</td>
                        <td class="curCours">
                            <div style="text-align:right">3,6627</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-xd"></i>
                                    <span class="text">СДР (Специальные права заимствования)</span>
                            </div>
                        </td>
                        <td class="curAmount">1 XDR</td>
                        <td class="curCours">
                            <div style="text-align:right">3,8943</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-sg"></i>
                                    <span class="text">Сингапурcкий доллар</span>
                            </div>
                        </td>
                        <td class="curAmount">1 SGD</td>
                        <td class="curCours">
                            <div style="text-align:right">2,1720</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-kg"></i>
                                    <span class="text">Сом</span>
                            </div>
                        </td>
                        <td class="curAmount">100 KGS</td>
                        <td class="curCours">
                            <div style="text-align:right">3,2957</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-kz"></i>
                                    <span class="text">Тенге</span>
                            </div>
                        </td>
                        <td class="curAmount">1000 KZT</td>
                        <td class="curCours">
                            <div style="text-align:right">6,4853</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-tr"></i>
                                    <span class="text">Турецкая лира</span>
                            </div>
                        </td>
                        <td class="curAmount">10 TRY</td>
                        <td class="curCours">
                            <div style="text-align:right">1,4806</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-gb"></i>
                                    <span class="text">Фунт стерлингов</span>
                            </div>
                        </td>
                        <td class="curAmount">1 GBP</td>
                        <td class="curCours">
                            <div style="text-align:right">3,6264</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-cz"></i>
                                    <span class="text">Чешская крона</span>
                            </div>
                        </td>
                        <td class="curAmount">100 CZK</td>
                        <td class="curCours">
                            <div style="text-align:right">13,5776</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-se"></i>
                                    <span class="text">Шведская крона</span>
                            </div>
                        </td>
                        <td class="curAmount">10 SEK</td>
                        <td class="curCours">
                            <div style="text-align:right">2,8120</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="curName">
                            <div class="country">
                                <i class="flag-icon flag-icon-ch"></i>
                                    <span class="text">Швейцарский франк</span>
                            </div>
                        </td>
                        <td class="curAmount">1 CHF</td>
                        <td class="curCours">
                            <div style="text-align:right">3,2507</div>
                        </td>
                    </tr>
            </tbody>
        </table>
        '''
        parsed = parse_currency_infos(html_raw)
        expected = [
            {'currency_name': 'Австралийский доллар', 'currency_amount': '1 AUD', 'currency_course': 1.9249},
            {'currency_name': 'Армянский драм', 'currency_amount': '1000 AMD', 'currency_course': 7.4559},
            {'currency_name': 'Болгарский лев', 'currency_amount': '1 BGN', 'currency_course': 1.6304},
            {'currency_name': 'Бразильский реал', 'currency_amount': '10 BRL', 'currency_course': 5.7774},
            {'currency_name': 'Гривна', 'currency_amount': '100 UAH', 'currency_course': 7.8128},
            {'currency_name': 'Датская крона', 'currency_amount': '10 DKK', 'currency_course': 4.2794},
            {'currency_name': 'Дирхам ОАЭ', 'currency_amount': '10 AED', 'currency_course': 7.8569},
            {'currency_name': 'Доллар США', 'currency_amount': '1 USD', 'currency_course': 2.8853},
            {'currency_name': 'Донг', 'currency_amount': '100000 VND', 'currency_course': 12.3054},
            {'currency_name': 'Евро', 'currency_amount': '1 EUR', 'currency_course': 3.1887},
            {'currency_name': 'Злотый', 'currency_amount': '10 PLN', 'currency_course': 6.9545},
            {'currency_name': 'Иена', 'currency_amount': '100 JPY', 'currency_course': 2.1435},
            {'currency_name': 'Индийская рупия', 'currency_amount': '100 INR', 'currency_course': 3.5273},
            {'currency_name': 'Иранский риал', 'currency_amount': '100000 IRR', 'currency_course': 6.8694},
            {'currency_name': 'Исландская крона', 'currency_amount': '100 ISK', 'currency_course': 2.1245},
            {'currency_name': 'Канадский доллар', 'currency_amount': '1 CAD', 'currency_course': 2.1201},
            {'currency_name': 'Китайский юань', 'currency_amount': '10 CNY', 'currency_course': 4.1657},
            {'currency_name': 'Кувейтский динар', 'currency_amount': '1 KWD', 'currency_course': 9.4198},
            {'currency_name': 'Молдавский лей', 'currency_amount': '10 MDL', 'currency_course': 1.6142},
            {'currency_name': 'Новозеландский доллар', 'currency_amount': '1 NZD', 'currency_course': 1.802},
            {'currency_name': 'Норвежская крона', 'currency_amount': '10 NOK', 'currency_course': 2.6974},
            {'currency_name': 'Российский рубль', 'currency_amount': '100 RUB', 'currency_course': 3.6627},
            {'currency_name': 'СДР (Специальные права заимствования)', 'currency_amount': '1 XDR',
             'currency_course': 3.8943},
            {'currency_name': 'Сингапурcкий доллар', 'currency_amount': '1 SGD', 'currency_course': 2.172},
            {'currency_name': 'Сом', 'currency_amount': '100 KGS', 'currency_course': 3.2957},
            {'currency_name': 'Тенге', 'currency_amount': '1000 KZT', 'currency_course': 6.4853},
            {'currency_name': 'Турецкая лира', 'currency_amount': '10 TRY', 'currency_course': 1.4806},
            {'currency_name': 'Фунт стерлингов', 'currency_amount': '1 GBP', 'currency_course': 3.6264},
            {'currency_name': 'Чешская крона', 'currency_amount': '100 CZK', 'currency_course': 13.5776},
            {'currency_name': 'Шведская крона', 'currency_amount': '10 SEK', 'currency_course': 2.812},
            {'currency_name': 'Швейцарский франк', 'currency_amount': '1 CHF', 'currency_course': 3.2507}
        ]
        self.assertEqual(parsed, expected)  # add assertion here

    def test_parse_currency_infos_should_fail(self):
        html_raw = 'aboba'
        with self.assertRaises(AttributeError):
            parse_currency_infos(html_raw)

    def test_parse_currency_info(self):
        html_raw = '''
        <tr>
            <td class="curName">
                <div class="country">
                    <i class="flag-icon flag-icon-au"></i>
                    <span class="text">Австралийский доллар</span>
                </div>
            </td>
            <td class="curAmount">1 AUD</td>
            <td class="curCours">
                <div style="text-align:right">1,9249</div>
            </td>
        </tr>
        '''
        soup = BeautifulSoup(html_raw, 'html.parser')
        cur_name, cur_amount, cur_course = parse_currency_info(soup)
        self.assertEqual(cur_name, 'Австралийский доллар')
        self.assertEqual(cur_amount, '1 AUD')
        self.assertAlmostEqual(cur_course, 1.9249)

    def test_parse_currency_info_should_fail(self):
        html_raw = '''
        <thead>
            <tr>
                <th>Наименование иностранной валюты</th>
                <th>Количество единиц иностранной валюты, буквенный код валюты</th>
                <th>Официальный курс</th>
            </tr>
        </thead>
        '''
        soup = BeautifulSoup(html_raw, 'html.parser')
        with self.assertRaises(AttributeError):
            parse_currency_info(soup)


if __name__ == '__main__':
    unittest.main()
