from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        import cms.api
        from django.contrib.sites.models import Site
        from django.contrib.auth.models import Group
        from pcart_catalog.cms_apps import CollectionApphook, ProductApphook
        from pcart_customers.cms_apps import CustomersApphook
        from pcart_cart.cms_apps import CartApphook
        from pcart_search.cms_apps import SearchApphook
        from pcart_customers.models import User
        from pcart_core.models import RootFile, ThemeSettings
        from pcart_catalog.models import ProductStatus
        from pcart_cart.models import OrderNumberFormat, OrderStatus
        from pcart_messaging.models import EmailTemplate
        from pcart_novaposhta.utils import update_nv_db
        from pcart_data_collections.models import DataCollection, DataCollectionField, WebForm

        admin_user = User.objects.filter(is_superuser=True).first()
        site = Site.objects.get(id=settings.SITE_ID)

        print('Create home page')
        home_page = cms.api.create_page(
            title='Домівка',
            template='index.html',
            language='uk',
            slug='home',
            published=True,
        )
        placeholder = home_page.placeholders.get(slot='main_content')
        cms.api.add_plugin(
            placeholder=placeholder,
            plugin_type='TextPlugin',
            language='uk',
            body='\n'.join(['<p>%s</p>' % x for x in lorem_ipsum.paragraphs(4)]),
        )
        cms.api.publish_page(home_page, admin_user, language='uk')
        print('Create collection app page')
        cms.api.create_page(
            title='Каталог',
            template='page.html',
            language='uk',
            slug='catalog',
            # in_navigation=False,
            apphook=CollectionApphook,
            apphook_namespace='pcart_collection',
            published=True,
        )
        print('Create product app page')
        cms.api.create_page(
            title='Товар',
            template='page.html',
            language='uk',
            slug='product',
            in_navigation=False,
            apphook=ProductApphook,
            apphook_namespace='pcart_product',
            published=True,
        )
        print('Create customer app page')
        cms.api.create_page(
            title='Клієнт',
            template='page.html',
            language='uk',
            slug='customer',
            in_navigation=False,
            apphook=CustomersApphook,
            apphook_namespace='pcart_customers',
            published=True,
        )
        print('Create cart app page')
        cms.api.create_page(
            title='Кошик',
            template='page.html',
            language='uk',
            slug='cart',
            in_navigation=False,
            apphook=CartApphook,
            apphook_namespace='pcart_cart',
            published=True,
        )

        print('Create search app page')
        cms.api.create_page(
            title='Пошук',
            template='page.html',
            language='uk',
            slug='search',
            in_navigation=False,
            apphook=SearchApphook,
            apphook_namespace='pcart_search',
            published=True,
        )

        print('Create warranty page')
        about_page = cms.api.create_page(
            title='Гарантія',
            template='page.html',
            language='uk',
            slug='warranty',
            published=True,
        )
        placeholder = about_page.placeholders.get(slot='main_content')
        cms.api.add_plugin(
            placeholder=placeholder,
            plugin_type='TextPlugin',
            language='uk',
            body='\n'.join(['<p>%s</p>' % x for x in lorem_ipsum.paragraphs(4)]),
        )
        cms.api.publish_page(about_page, admin_user, language='uk')

        print('Create payment page')
        contact_page = cms.api.create_page(
            title='Оплата',
            template='page.html',
            language='uk',
            slug='payment',
            published=True,
        )
        placeholder = contact_page.placeholders.get(slot='main_content')
        cms.api.add_plugin(
            placeholder=placeholder,
            plugin_type='TextPlugin',
            language='uk',
            body='\n'.join(['<p>%s</p>' % x for x in lorem_ipsum.paragraphs(4)]),
        )
        cms.api.publish_page(contact_page, admin_user, language='uk')

        print('Create contact page')
        contact_page = cms.api.create_page(
            title='Контакти',
            template='page.html',
            language='uk',
            slug='contacts',
            published=True,
        )
        placeholder = contact_page.placeholders.get(slot='main_content')
        cms.api.add_plugin(
            placeholder=placeholder,
            plugin_type='TextPlugin',
            language='uk',
            body='\n'.join(['<p>%s</p>' % x for x in lorem_ipsum.paragraphs(4)]),
        )
        cms.api.publish_page(contact_page, admin_user, language='uk')

        print('Init users groups')
        order_group = Group.objects.create(name='order')

        print('Create robots.txt')
        RootFile.objects.create(
            site=site,
            file_name='robots.txt',
            content='User-agent: *\nDisallow: /\n',
        )

        print('Init theme settings')
        ThemeSettings.objects.create(
            site=site,
            data={
                "product_desc_color": "#999999",
                "megamenu_link": "/catalog/",
                "product_desc_size": "11px",
                "show_copyright": True,
                "cookies_policy_tagline": "Ми використовуємо куки (cookies) для роботи системи авторизації користувачів.",
                "sidebar_toggle": "sidebar_toggle_left",
                "product_name_color_hover": "#00ab4e",
                "cookies_policy_expire": "30",
                "color_4": "#00ab4e",
                "megamenu_text": "Каталог",
                "homepage_info_bg_toggle": True,
                "newsletter_mailchimp_url": "#",
                "cookies_policy_toggle": False,
                "newsletter_form_type": "newsletter_shopify",
                "product_name_size": "14px",
                "cookies_policy_text": "If you do nothing, we'll assume that's OK.",
                "newsletter_popup_disable": "365",
                "base_font_color": "#777777",
                "use_logo": True,
                "product_price_color": "#f6b220",
                "border_color": "#d9d9d9",
                "homepage_info_bg.jpg": None,
                "newsletter_popup_title": "Підпишіться на нашу розсилку щоб бути в курсі свіжих новин",
                "heading_font_size": "32px",
                "link_color": "#00ab4e",
                "newsletter_popup_toggle": True,
                "logo.png": None,
                "new_products_period": "100000",
                "product_price_sale_color": "#f54040",
                "color_1": "#ffffff",
                "megamenu_show_full_link": False,
                "favicon.ico": None,
                "link_color_hover": "#333333",
                "body_bg_color": "#ffffff",
                "heading_font": "google_fonts:Roboto Condensed",
                "heading_font_color": "#333333",
                "cookies_policy_redirect": "#",
                "megamenu_sub_toggle": True,
                "body_bg_img.jpg": None,
                "megamenu_badge": "",
                "logo_slogan": "",
                "color_5": "#f6b220",
                "color_2": "#333333",
                "newsletter_popup_bg_toggle": True,
                "product_name_color": "#333333",
                "base_font_size": "14px",
                "color_3": "#00553c",
                "body_bg_img_toggle": False,
                "base_font": "google_fonts:Roboto Condensed",
            }
        )

        print('Create product statuses')
        ProductStatus.objects.create(
            title='Архів', show_buy_button=False, is_visible=False, is_searchable=False, weight=0)
        ProductStatus.objects.create(
            title='Немає в наявності', show_buy_button=False, is_searchable=False, weight=2)
        ProductStatus.objects.create(
            title='Очікується', show_buy_button=True, weight=4)
        ProductStatus.objects.create(
            title='В наявності', show_buy_button=True, weight=6)

        print('Create order numbers template')
        OrderNumberFormat.objects.create(site=site)

        print('Create order statuses')
        OrderStatus.objects.filter(slug='submitted').delete()
        OrderStatus.objects.create(title='Новий', slug='submitted', weight=0)
        OrderStatus.objects.create(title='Оброблюється', slug='processing', weight=2)
        OrderStatus.objects.create(title='Доставляється', slug='shipping', weight=4)
        OrderStatus.objects.create(title='Доставлено', slug='shipped', weight=6)
        OrderStatus.objects.create(title='Відмінено', slug='cancelled', weight=8)

        print('Init Nova-Poshta offices')
        update_nv_db()

        print('Init email templates')
        _template = '''
<mjml>
  <mj-body>
    <mj-container>
      <mj-section>
        <mj-column>
          <mj-text font-weight="bold" font-size="22" align="center">{{site}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
        <mj-column>
          <mj-text>Замовлення {{order.number}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
         <mj-column>
           <mj-table>
             <tr>
               <th align="left">Товар</th>
               <th align="left">Ціна позиції</th>
             </tr>
           {% for item in order.items %}
           <tr>
             <td>{{item.object.title}}</td>
             <td>{{item.quantity}} &times; {{item.price|money}} = {{item.line_price|money}}</td>
           </tr>
           {% endfor %}
           </mj-table>
           <mj-divider border-width="1px" border-style="dashed" border-color="lightgrey" />
           <mj-text font-weight="bold">Subtotal: {{order.total_price|money}}</mj-text>
           <mj-text>{{order.note}}</mj-text>
           <mj-text>
          {% if format == "html" %}
          {{order.get_shipping_info}}
          {% else %}
          {{order.get_shipping_info_as_text}}
          {% endif %}
          </mj-text>
           <mj-text>
          {% if format == "html" %}
          {{order.get_payment_info}}
          {% else %}
          {{order.get_payment_info_as_text}}
          {% endif %}
          </mj-text>
         </mj-column>
      </mj-section>
    </mj-container>
  </mj-body>
</mjml>
'''

        EmailTemplate.objects.create(
            name='order',
            subject='Замовлення {{order.number}} прийнято',
            mjml_template=_template,
        )

        _template = '''
<mjml>
  <mj-body>
    <mj-container>
      <mj-section>
        <mj-column>
          <mj-text font-weight="bold" font-size="22" align="center">{{site}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
        <mj-column>
          <mj-text>Замовлення {{order.number}} від {{order.customer}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
         <mj-column>
           <mj-table>
             <tr>
               <th align="left">Товар</th>
               <th align="left">Ціна позиции</th>
             </tr>
           {% for item in order.items %}
           <tr>
             <td>{{item.object.title}}</td>
             <td>{{item.quantity}} &times; {{item.price|money}} = {{item.line_price|money}}</td>
           </tr>
           {% endfor %}
           </mj-table>
           <mj-divider border-width="1px" border-style="dashed" border-color="lightgrey" />
           <mj-text font-weight="bold">Subtotal: {{order.total_price|money}}</mj-text>
           <mj-text>{{order.note}}</mj-text>
           <mj-text>
          {% if format == "html" %}
          {{order.get_shipping_info}}
          {% else %}
          {{order.get_shipping_info_as_text}}
          {% endif %}
          </mj-text>
           <mj-text>
          {% if format == "html" %}
          {{order.get_payment_info}}
          {% else %}
          {{order.get_payment_info_as_text}}
          {% endif %}
          </mj-text>
         </mj-column>
      </mj-section>
    </mj-container>
  </mj-body>
</mjml>
'''

        EmailTemplate.objects.create(
            name='order_moderation',
            subject='Нове замовлення {{order.number}} на {{order.site}}',
            mjml_template=_template,
        )

        _template = '''
<mjml>
  <mj-body>
    <mj-container>
      <mj-section>
        <mj-column>
          <mj-text font-weight="bold" font-size="22" align="center"> {{site}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
        <mj-column>
          <mj-text>Скидання пароля</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
         <mj-column>
           <mj-text>Ви запитали скидання пароля на сайті {{site}}. Для продовження натисніть на кнопку:</mj-text>
           <mj-button background-color="orange" href="https://{{site.domain}}{{reset_link.get_absolute_url}}">Встановити новий пароль</mj-button>
         </mj-column>
      </mj-section>
    </mj-container>
  </mj-body>
</mjml>
'''

        EmailTemplate.objects.create(
            name='reset_password',
            subject='Скидання пароля на {{site}}',
            mjml_template=_template,
        )

        _template = '''
<mjml>
  <mj-body>
    <mj-container>
      <mj-section>
        <mj-column>
          <mj-text font-weight="bold" font-size="22" align="center">{{site}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
        <mj-column>
          <mj-text>Реєстрація користувача</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
         <mj-column>
           <mj-text>Вітаємо, {{reset_link.user.customer.name}}!</mj-text>
           <mj-text>Тепер у Вас є власний акаунт в магазині {{site}}.
           В якості логіна використовуйте адресу своєї електронної пошти або телефон:
            <dl>
              <dt>Email:</dt><dd>{{reset_link.user.email}}</dd>
              <dt>Телефон:</dt><dd>{{reset_link.user.phone}}</dd>
            </dl>
           </mj-text>
           <mj-text>Ваш аккаунт було створено автоматично, тому він поки не має
           встановленого пароля і в нього неможливо увійти. Натисніть на кнопку нижче, щоб
           перейти до форми встановлення пароля й завершити реєстрацію.</mj-text>
           <mj-button background-color="orange" href="https://{{site.domain}}{{reset_link.get_absolute_url}}">Встановити пароль</mj-button>
         </mj-column>
      </mj-section>
    </mj-container>
  </mj-body>
</mjml>
'''

        EmailTemplate.objects.create(
            name='setup_password',
            subject='Реєстрація користувача на {{site}}',
            mjml_template=_template,
        )

        _template = '''
<mjml>
  <mj-body>
    <mj-container>
      <mj-section>
        <mj-column>
          <mj-text font-weight="bold" font-size="22" align="center">{{site}}</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
        <mj-column>
          <mj-text>Замовлення в 1 клік</mj-text>
        </mj-column>
      </mj-section>
      <mj-section>
         <mj-column>
           <mj-text>Користувач заповнив на сайті форму купівлі товару в 1 клік.</mj-text>
           <mj-text>
            <dl>
              <dt>Телефон:</dt><dd>{{title}}</dd>
              <dt>Товар:</dt><dd><a href="https://{{site.domain}}/products/{{product_slug}}/">https://{{site.domain}}/products/{{product_slug}}/</a></dd>
            </dl>
           </mj-text>
           <mj-button background-color="orange" href="https://{{site.domain}}/products/{{product_slug}}/">Перейти на сторінку товару</mj-button>
         </mj-column>
      </mj-section>
    </mj-container>
  </mj-body>
</mjml>
'''

        EmailTemplate.objects.create(
            name='one_click_purchase',
            subject='Замовлення в 1 клік на {{site}}',
            mjml_template=_template,
        )

        print('1 click feature')
        data_collection = DataCollection.objects.create(
            title='one-click-purchase',
            title_field_label='Телефон',
            reversed_ordering=True,
        )
        DataCollectionField.objects.create(
            data_collection=data_collection,
            name='product_slug',
            title='Товар',
            required=True,
        )

        WebForm.objects.create(
            title='one-click-purchase',
            data_collection=data_collection,
            fields='title,product_slug',
            hidden_fields='product_slug',
        )

        print('Done')
