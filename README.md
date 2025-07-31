# django_ecommerce_beta
Django Beta project for a real ecommerce website.
All the code in this project is AI generated. The purpose of this project is to learn from AI how to do a fully functional and realistic ecommerce site to replicate and use to sell stuff online. Also, I'm planning on using this project as a base template to sell ecommerce sites to clients. 


Payment Integration 
- 1.  🛒 **Session-based shopping cart:** The cart is tied to the user’s session
    
    **Stateless and Scalable:** it does not require saving the cart to the database unless extended to Logged-in users (later on). 
    
    **Persistent for logged-in users:** The cart can be saved to the database for logged-in users to review it later.


- 2. **The checkout flow:** Multistep checkout view. Shipping → Payment
    1. Cart review: Display the items in the cart.
    2. Shipping information: User selects their shipping `address` .
    3. Payment method selection: PSE, Mercado-pago, Wompi? 
    4. Order confirmation: A final summary of the order before payment.

- 3. **Payment gateway Integration: AI suggestion: Mercado Pago:**
 https://www.mercadopago.com.co/developers/es/docs/checkout-api/additional-content/your-integrations/introduction
    
    Mercado Pago supports a variety of payment methods in Colombia-including PSE, and provides good developer documentation.

- 4. **Order Management**
    1. Update the `order` model’ status based on the payment gateway’s response.
    2. Create an order confirmation page and send a confirmation email to the user.
    3. Build a view for users to see their order history.


LAST Gemini response

Okay, I will update your ecommerce/ecommerce/settings.py file with
  placeholder ngrok URLs for the Mercado Pago back_urls.


  Important: These are placeholder URLs. You must replace YOUR_NGROK_URL_HERE
  with the actual https forwarding URL that ngrok provides when you run ngrok
  http 8000. This URL changes every time you start ngrok (unless you have a
  paid ngrok account with a static domain).


  Here's the change I'll make:
 ╭───────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ecommerce\ecommerce\settings.py: MERCADO_PAGO_ACCESS_TOKEN = os... =… │
 │                                                                               │
 │    146                                                                        │
 │    147                                                                        │
 │    148                                                                        │
 │    149  + # Mercado Pago API credentials and return URLs                      │
 │    150  + # IMPORTANT: Replace 'YOUR_MERCADO_PAGO_ACCESS_TOKEN'               │
 │           with your actual Mercado Pago Access Token.                         │
 │    151  + # For testing, use your Sandbox Access Token.                       │
 │    152    MERCADO_PAGO_ACCESS_TOKEN =                                         │
 │           os.getenv('MERCADO_PAGO_ACCESS_TOKEN')                              │
 │    150  - MERCADO_PAGO_SUCCESS_URL =                                          │
 │           'http://127.0.0.1:8000/payment/success/'                            │
 │    151  - MERCADO_PAGO_FAILURE_URL =                                          │
 │           'http://127.0.0.1:8000/payment/failure/'                            │
 │    152  - MERCADO_PAGO_PENDING_URL =                                          │
 │           'http://127.0.0.1:8000/payment/pending/'                            │
 │    153  +                                                                     │
 │    154  + # Mercado Pago return URLs after payment.                           │
 │    155  + # IMPORTANT: When testing with Mercado Pago, these URLs             │
 │           MUST be publicly accessible.                                        │
 │    156  + # During local development, you will need to use a tool             │
 │           like ngrok to expose your local server.                             │
 │    157  + # Replace 'YOUR_NGROK_URL_HERE' with the actual HTTPS               │
 │           forwarding URL provided by ngrok                                    │
 │    158  + # (e.g., https://abcdef12345.ngrok-free.app).                       │
 │    159  + MERCADO_PAGO_SUCCESS_URL =                                          │
 │           'YOUR_NGROK_URL_HERE/payment/success/'                              │
 │    160  + MERCADO_PAGO_FAILURE_URL =                                          │
 │           'YOUR_NGROK_URL_HERE/payment/failure/'                              │
 │    161  + MERCADO_PAGO_PENDING_URL =                                          │
 │           'YOUR_NGROK_URL_HERE/payment/pending/'                              │
 ╰───────────────────────────────────────────────────────────────────────────────╯
✦ I have updated your ecommerce/ecommerce/settings.py file with comments and
  placeholder URLs for Mercado Pago.

  Next Steps (which you need to perform manually):


   1. Run ngrok: Open your command prompt, navigate to where you extracted
      ngrok.exe, and run:

   1     ngrok http 8000

      Keep this window open.
   2. Get the HTTPS Forwarding URL: From the ngrok output, copy the https
      forwarding URL (it will look something like
      https://<random_string>.ngrok-free.app).
   3. Update `settings.py`: Open ecommerce/ecommerce/settings.py and replace all
      instances of 'YOUR_NGROK_URL_HERE' with the actual HTTPS ngrok URL you just
       copied.
   4. Restart Django Server: After updating settings.py, you must restart your
      Django development server for the changes to take effect.


  Once these steps are completed, try the checkout process again. The Mercado
  Pago preference creation should now succeed, and you should be redirected to
   the Mercado Pago payment page.

