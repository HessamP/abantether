# Abantether test
- **user signup:** `POST /api/user/signup/`
- **user login:** `POST /api/user/login/`
- **place order:** `POST /api/order/`

for detail of payload please use Postman collection


## Balance Description
- created 2 users with proper amount of balance 
  - **blocked_amount**: This field represents the portion of the user's balance that is temporarily unavailable for use 
  - **amount**: This field represents the total balance in the user's account
  

  <div style="display: grid; justify-content: space-around;">
  <img src="image/balance.png" alt="Anomaly" >
</div>

## Order descriptions

1- user1 orders a quantity of ABAN token which the amount exceeds 10$, as assignment sample lets say 3 ABAN:

 <div style="display: grid; justify-content: space-around;">
  <img src="image/3token.png" alt="Anomaly" >
</div>

12$ will locked first then after calling buy_from_exchange() it deducted from balance(amount) so we will have:\
balance(user1):

<div style="display: grid; justify-content: space-around;">
  <img src="image/balance1.png" alt="Anomaly" >
</div>

then the orders will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/order1.png" alt="Anomaly" >
</div>

now, an order for just 1 ABAN:

<div style="display: grid; justify-content: space-around;">
  <img src="image/order1token.png" alt="Anomaly" >
</div>

balance will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/balanceafter1.png" alt="Anomaly" >
</div>

and orders will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/orderafter1.png" alt="Anomaly" >
</div>

now another 1 token but with user2.
balance will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/balanceafter2.png" alt="Anomaly" >
</div>

and orders will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/ordersafter2.png" alt="Anomaly" >
</div>

now for last order by user2 we expect to run buy_from_exchange() and synchronize all associated statuses:
balance will be:

<div style="display: grid; justify-content: space-around;">
  <img src="image/lastbalance.png" alt="Anomaly" >
</div>

and the orders:

<div style="display: grid; justify-content: space-around;">
  <img src="image/lastorder.png" alt="Anomaly" >
</div>