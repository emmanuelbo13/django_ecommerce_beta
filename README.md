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



