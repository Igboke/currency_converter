# CURRENCY CONVERTER API

Implementation of [Fawaz Ahmed API](https://github.com/fawazahmed0/exchange-api)

## 📌 Features

- Convert an amount between two currencies (crypto or fiat)
- Fetch current exchange rates
- List all available currencies
- Basic Authentication and Cookie-based Authentication

---

## 📂 Endpoints

### 🔄 `POST /api/v1/convert/`

**Description:** Converts a specified amount from one currency to another using the latest exchange rate.

**Request Body:**
Content Types: `application/json`, `application/x-www-form-urlencoded`

| Field              | Type   | Description                         | Required |
|-------------------|--------|-------------------------------------|----------|
| base_currency      | string | Code of the currency to convert from | ✅       |
| converted_currency | string | Code of the currency to convert to   | ✅       |
| amount             | string | Amount to be converted               | ✅       |
| date               | string | Optional date (YYYY-MM-DD)           | ❌       |

**Response Example:**

```json
{
  "base_currency": "USD",
  "converted_currency": "EUR",
  "original_amount": "100.00",
  "exchange_rate": "0.89",
  "calculated_amount": "89.00",
  "date": "2025-05-01"
}
```
---

### 📄 GET /api/v1/currencies/

```json
[
  {
    "code": "USD",
    "name": "United States Dollar"
  },
  {
    "code": "BTC",
    "name": "Bitcoin"
  }
]
```

For questions or feedback, please contact:
- **Email**: danieligboke669@gmail.com
- **GitHub**: [Igboke](https://github.com/Igboke)
- **Project Website**: [Currency Converter](https://currency-converter-i7w7.onrender.com/api/schema/swagger-ui/)