import pandas as pd
import streamlit as st

st.set_page_config(page_title="Automatic Petrol Cars Under ₹10L", page_icon="🚗", layout="wide")

IMG = "https://stimg.cardekho.com/images/cms/carnewsimages/editorimages/"

# Ex-showroom (Delhi), entry automatic variant. Source: CarDekho, Aug 2026.
# Mileage = claimed (ARAI) figure for the model range; None = not listed.
CARS = [
    dict(name="Maruti S-Presso", variant="VXi (O) AGS", price=4.75, body="Hatchback", seats=5,
         engine="1.0L petrol", turbo=False, power=68, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=24.76, img=IMG + "6a745cda8c450.jpg"),
    dict(name="Maruti Wagon R", variant="VXi AGS", price=5.97, body="Hatchback", seats=5,
         engine="1.0L / 1.2L petrol", turbo=False, power=None, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=24.35, img=IMG + "6a745a7f60af7.jpg"),
    dict(name="Tata Tiago", variant="Pure AMT", price=6.00, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=None, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=None, img=IMG + "6a745994b29bb.jpg"),
    dict(name="Maruti Swift", variant="VXi AGS", price=7.08, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=82, torque=112, gearbox="AMT", speeds="5-speed",
         mileage=25.35, img=IMG + "6a745ad738cab.jpg"),
    dict(name="Tata Altroz", variant="Pure AMT", price=7.70, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=88, torque=115, gearbox="AMT", speeds="5-speed",
         mileage=None, img=IMG + "6a745de20afe4.jpg"),
    dict(name="Hyundai i20", variant="Magna IVT", price=8.13, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=None, torque=None, gearbox="CVT", speeds="IVT",
         mileage=16.0, img=IMG + "6a745b4055080.jpg"),
    dict(name="Renault Triber", variant="Emotion AMT", price=8.48, body="MPV", seats=7,
         engine="1.0L petrol", turbo=False, power=72, torque=96, gearbox="AMT", speeds="5-speed",
         mileage=20.0, img=IMG + "6a745f2d88e0f.jpg"),
    dict(name="Honda Amaze", variant="V CVT", price=8.70, body="Sedan", seats=5,
         engine="1.2L petrol", turbo=False, power=90, torque=110, gearbox="CVT", speeds="7-step",
         mileage=18.65, img=IMG + "6a745beacc156.JPG"),
    dict(name="Tata Nexon", variant="Smart+ AMT", price=8.90, body="Compact SUV", seats=5,
         engine="1.2L turbo-petrol", turbo=True, power=120, torque=170, gearbox="AMT", speeds="6-speed",
         mileage=17.44, img=IMG + "6a745c35a7b66.jpg"),
    dict(name="Mahindra XUV 3XO", variant="MX2 Pro AT", price=9.99, body="Compact SUV", seats=5,
         engine="1.2L turbo-petrol", turbo=True, power=110, torque=200, gearbox="Automatic (TC)", speeds="6-speed",
         mileage=18.89, img=IMG + "6a745df8d8f8f.jpg"),
]

df = pd.DataFrame(CARS)

# ---------------------------------------------------------------- sidebar filters
st.sidebar.header("🔎 Filters")

search = st.sidebar.text_input("Search by name", placeholder="e.g. Swift")

price_min, price_max = float(df.price.min()), 10.0
budget = st.sidebar.slider("Ex-showroom price (₹ lakh)", price_min, price_max,
                           (price_min, price_max), step=0.25)

body_types = st.sidebar.multiselect("Body type", sorted(df.body.unique()), default=sorted(df.body.unique()))
gearboxes = st.sidebar.multiselect("Transmission", sorted(df.gearbox.unique()), default=sorted(df.gearbox.unique()))
seats = st.sidebar.radio("Seating", ["Any", "5", "7"], horizontal=True)
engine_type = st.sidebar.radio("Engine", ["Any", "Turbo only", "Naturally aspirated only"])

min_mileage = st.sidebar.slider("Min claimed mileage (kmpl)", 0, 30, 0)
min_power = st.sidebar.slider("Min power (PS)", 0, 130, 0, step=5)
st.sidebar.caption("Mileage/power filters hide cars whose figures aren't listed.")

sort_by = st.sidebar.selectbox("Sort by", ["Price (low → high)", "Price (high → low)",
                                           "Mileage (high → low)", "Power (high → low)"])

# ---------------------------------------------------------------- apply filters
f = df.copy()
if search:
    f = f[f.name.str.contains(search, case=False)]
f = f[f.price.between(*budget)]
f = f[f.body.isin(body_types) & f.gearbox.isin(gearboxes)]
if seats != "Any":
    f = f[f.seats == int(seats)]
if engine_type == "Turbo only":
    f = f[f.turbo]
elif engine_type == "Naturally aspirated only":
    f = f[~f.turbo]
if min_mileage:
    f = f[f.mileage.fillna(-1) >= min_mileage]
if min_power:
    f = f[f.power.fillna(-1) >= min_power]

sorters = {
    "Price (low → high)": ("price", True),
    "Price (high → low)": ("price", False),
    "Mileage (high → low)": ("mileage", False),
    "Power (high → low)": ("power", False),
}
col, asc = sorters[sort_by]
f = f.sort_values(col, ascending=asc, na_position="last").reset_index(drop=True)

# ---------------------------------------------------------------- header
st.title("🚗 Petrol Automatic Cars Under ₹10 Lakh")
st.caption("Ex-showroom Delhi prices for the cheapest automatic variant. Source: CarDekho (Aug 2026). "
           "On-road price in your city will be ~10–15% higher.")

c1, c2, c3 = st.columns(3)
c1.metric("Cars matching", len(f))
if len(f):
    c2.metric("Cheapest", f"₹{f.price.min():.2f} L")
    best = f.mileage.max()
    c3.metric("Best mileage", f"{best:.1f} kmpl" if pd.notna(best) else "—")

if f.empty:
    st.warning("No cars match these filters. Try loosening them.")
    st.stop()


def fmt(v, suffix=""):
    return "—" if pd.isna(v) else f"{v:g}{suffix}"


tab_cards, tab_table, tab_compare, tab_chart = st.tabs(["🖼️ Cards", "📋 Table", "⚖️ Compare", "📊 Chart"])

# ---------------------------------------------------------------- cards
with tab_cards:
    cols = st.columns(3)
    for i, r in f.iterrows():
        with cols[i % 3].container(border=True):
            try:
                st.image(r.img, use_container_width=True)
            except Exception:
                st.write("🖼️ Image unavailable")
            st.subheader(r["name"])
            st.caption(f"{r.variant} · {r.body} · {r.seats} seats")
            st.markdown(f"### ₹{r.price:.2f} L")
            st.markdown(
                f"- **Engine:** {r.engine}\n"
                f"- **Power / Torque:** {fmt(r.power, ' PS')} / {fmt(r.torque, ' Nm')}\n"
                f"- **Gearbox:** {r.speeds} {r.gearbox}\n"
                f"- **Mileage:** {fmt(r.mileage, ' kmpl')}"
            )

# ---------------------------------------------------------------- table
with tab_table:
    table = f.assign(
        **{"Price (₹ L)": f.price, "Power (PS)": f.power, "Torque (Nm)": f.torque, "Mileage (kmpl)": f.mileage,
           "Gearbox": f.speeds + " " + f.gearbox}
    )[["name", "variant", "body", "seats", "Price (₹ L)", "engine", "Power (PS)", "Torque (Nm)",
       "Gearbox", "Mileage (kmpl)"]].rename(columns={"name": "Car", "variant": "Variant", "body": "Body",
                                                    "seats": "Seats", "engine": "Engine"})
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download CSV", table.to_csv(index=False), "cars_under_10_lakh.csv", "text/csv")

# ---------------------------------------------------------------- compare
with tab_compare:
    picks = st.multiselect("Pick 2–3 cars to compare", f.name.tolist(), max_selections=3)
    if len(picks) >= 2:
        sel = f[f.name.isin(picks)].set_index("name")
        cmp = pd.DataFrame({
            "Variant": sel.variant,
            "Price (₹ L)": sel.price.map("{:.2f}".format),
            "Body": sel.body,
            "Seats": sel.seats,
            "Engine": sel.engine,
            "Power (PS)": sel.power.map(fmt),
            "Torque (Nm)": sel.torque.map(fmt),
            "Gearbox": sel.speeds + " " + sel.gearbox,
            "Mileage (kmpl)": sel.mileage.map(fmt),
        }).T
        st.dataframe(cmp, use_container_width=True)
    else:
        st.info("Select at least two cars.")

# ---------------------------------------------------------------- chart
with tab_chart:
    metric = st.selectbox("Metric", ["price", "mileage", "power", "torque"])
    chart_df = f.set_index("name")[metric].dropna()
    if chart_df.empty:
        st.info("No data for this metric in the current selection.")
    else:
        st.bar_chart(chart_df)

st.caption("Specs vary by variant. Confirm final prices, features and mileage with your dealer.")
