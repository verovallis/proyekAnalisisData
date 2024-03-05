import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from babel.numbers import format_currency
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("/Users/wibisono/Downloads/Bangkit/projectDicoding/dashboard/allData.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
all_df['order_approved_at'] = pd.to_datetime(all_df['order_approved_at'])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("/Users/wibisono/Downloads/Bangkit/projectDicoding/dashboard/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]

# Judul
st.title("Welcome to E-Commerce Dashboard :convenience_store:")

totalPenjualan_df = main_df.groupby("product_category_name")["product_id"].count().reset_index()
totalPenjualan_df = totalPenjualan_df.rename(columns={"product_category_name": "Products Name", "product_id": "Products ID"})
totalPenjualan_df = totalPenjualan_df.sort_values(by="Products ID", ascending=False).head(10)

#T op 10 Penjualan Produk
st.header('Top 10 Penjualan Produk')

# Membagi layout jadi 2 kolom
col1, col2 = st.columns(2)

# Menampilkan total produk terjual dalam kolom pertama
with col1:
    st.dataframe(totalPenjualan_df)

# Menambilkan Bar chart di Kolom kedua
with col2:
    st.write("Bar Chart Top 10 Penjualan Produk:")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(totalPenjualan_df['Products Name'], totalPenjualan_df['Products ID'], color='skyblue')
    plt.xlabel('Product Category')
    plt.ylabel('Number of Products Sold')
    plt.title('Top 10 Penjualan Produk')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Display chart
    st.pyplot(fig)


# Customer Satisfaction
st.header('Customer Satisfaction')

product_ratings = all_df.groupby('product_category_name')['review_score'].mean().reset_index()

# mengurutkan produk berdasarkan review score
sorted_products = product_ratings.sort_values(by='review_score', ascending=False)

# mencari rating produk tertinggi
highest_rated_product = sorted_products.iloc[0]

# mencari rating produk terendah
lowest_rated_product = sorted_products.iloc[-1]

# Display results
st.subheader("Product Ratings")
st.write("Highest Rated Product:")
st.write(highest_rated_product)
st.write("\nLowest Rated Product:")
st.write(lowest_rated_product)

# Rating Distribution
st.write("Rating Distribution:")
rating_scores = all_df['review_score'].value_counts().sort_index()

plt.figure(figsize=(8, 5))
sns.barplot(x=rating_scores.index, y=rating_scores.values, palette="viridis")
plt.title("Customer Rating Distribution", fontsize=15)
plt.xlabel("Rating", fontsize=12)
plt.ylabel("Total Count", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot()


# Product Ratings
st.write("Product Ratings:")
product_ratings = all_df.groupby('product_category_name')['review_score'].mean().reset_index().sort_values(by='review_score', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='review_score', y='product_category_name', data=product_ratings, palette="plasma")
plt.title("Average Product Rating by Category", fontsize=15)
plt.xlabel("Average Rating", fontsize=12)
plt.ylabel("Product Category", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

#performa penjualan 
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Extract month and year
all_df['bulan'] = all_df['order_purchase_timestamp'].dt.to_period('M')

# Group by bulan dan melakukan kalkulasi
penjualan_per_bulan = all_df.groupby('bulan')['price'].agg(['sum', 'mean']).reset_index()

penjualan_per_bulan['bulan'] = penjualan_per_bulan['bulan'].astype(str) + '-01'
penjualan_per_bulan['bulan'] = pd.to_datetime(penjualan_per_bulan['bulan'])

st.header("Performa Penjualan")

# Display data table
st.write(penjualan_per_bulan)

# Plot
st.subheader("Grafik Performa Penjualan")
plt.figure(figsize=(10, 6))
plt.plot(penjualan_per_bulan['bulan'], penjualan_per_bulan['sum'], marker='o', color='b', linestyle='-')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan')
plt.title('Total Penjualan per Bulan')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Display the plot
st.pyplot(plt)

st.caption('Copyright (C) Valliska Noviana Wibisono - Project Dicoding - Bangkit. 2024')