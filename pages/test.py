import streamlit as st


def styles():
    return """
    <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #121212;
          color: #fff;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 20px 0;
        }
        th,
        td {
          padding: 12px;
          text-align: left;
          border-bottom: 1px solid #ddd;
        }
        th {
          background-color: #333;
        }
        tr:hover {
          background-color: #444;
        }
        .edit-btn {
          background-color: #4caf50;
          color: white;
          border: none;
          padding: 5px 10px;
          cursor: pointer;
        }
        .edit-btn:hover {
          background-color: #45a049;
        }
      </style>
  """


def rows(transactions):
    tr = []
    for transaction in transactions:
        tr.append(f"""
          <tr>
            <td>{transaction["ativo"]}</td>
            <td>{transaction["qtd"]}</td>
            <td>R$ {transaction["price"]}</td>
            <td>{transaction["date"]}</td>
            <td>R$ {transaction["total"]}</td>
            <td><button class="edit-btn">Editar</button></td>
          </tr>
    """)

    return " ".join(tr)


def table(transactions):
    return f"""
    <body>
      {styles()}
      <table>
        <thead>
          <tr>
            <th>Ativo</th>
            <th>Quantidade</th>
            <th>Preço</th>
            <th>Data da Compra</th>
            <th>Total</th>
            <th>Editar</th>
          </tr>
        </thead>
        <tbody>
          {rows(transactions)}
        </tbody>
      </table>
    </body>
  """


def transaction_table():
    st.html(
        table([{
            "_id": {
                "$oid": "668ffbd031dc4a3d65912322"
            },
            "ativo": "BTLG11",
            "qtd": 2,
            "price": 94.66,
            "date": "03/05/23",
            "total": 189.32,
            "user_id": {
                "$oid": "668e76af007f1d8109df7b35"
            }
        }])
    )


transaction_table()
