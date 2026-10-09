import pandas as pd
import streamlit as st

st.set_page_config(page_title="Automatic Petrol Cars Under ₹10L", page_icon="🚗", layout="wide")

IMG = "https://stimg.cardekho.com/images/cms/carnewsimages/editorimages/"

# ------------------------------------------------------------------ DATA
# price         = ex-showroom (Delhi, ₹ lakh) of the cheapest automatic variant (CarDekho, Aug 2026)
# sunroof_price = ex-showroom of the cheapest AUTOMATIC variant that has a sunroof (Autocar India, Mar 2026)
# base_known    = False -> `price` is already the sunroof variant's price (base automatic price not checked)
# Mileage = claimed figure for the model range; None = not listed.
CARS = [
    dict(name="Maruti S-Presso", variant="VXi (O) AGS", price=4.75, body="Hatchback", seats=5,
         engine="1.0L petrol", turbo=False, power=68, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=24.76, img=IMG + "6a745cda8c450.jpg",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Maruti Wagon R", variant="VXi AGS", price=5.97, body="Hatchback", seats=5,
         engine="1.0L / 1.2L petrol", turbo=False, power=None, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=24.35, img=IMG + "6a745a7f60af7.jpg",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Tata Tiago", variant="Pure AMT", price=6.00, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=None, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=None, img=IMG + "6a745994b29bb.jpg",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Maruti Swift", variant="VXi AGS", price=7.08, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=82, torque=112, gearbox="AMT", speeds="5-speed",
         mileage=25.35, img=IMG + "6a745ad738cab.jpg",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Tata Altroz", variant="Pure AMT", price=7.70, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=88, torque=115, gearbox="AMT", speeds="5-speed",
         mileage=None, img=IMG + "6a745de20afe4.jpg",
         sunroof=True, sunroof_price=7.91, sunroof_variant="Pure S AMT"),
    dict(name="Hyundai i20", variant="Magna IVT", price=8.13, body="Hatchback", seats=5,
         engine="1.2L petrol", turbo=False, power=None, torque=None, gearbox="CVT", speeds="IVT",
         mileage=16.0, img=IMG + "6a745b4055080.jpg",
         sunroof=True, sunroof_price=8.13, sunroof_variant="Magna IVT"),
    dict(name="Renault Triber", variant="Emotion AMT", price=8.48, body="MPV", seats=7,
         engine="1.0L petrol", turbo=False, power=72, torque=96, gearbox="AMT", speeds="5-speed",
         mileage=20.0, img=IMG + "6a745f2d88e0f.jpg",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Honda Amaze", variant="V CVT", price=8.70, body="Sedan", seats=5,
         engine="1.2L petrol", turbo=False, power=90, torque=110, gearbox="CVT", speeds="7-step",
         mileage=18.65, img=IMG + "6a745beacc156.JPG",
         sunroof=False, sunroof_price=None, sunroof_variant=None),
    dict(name="Tata Nexon", variant="Smart+ AMT", price=8.90, body="Compact SUV", seats=5,
         engine="1.2L turbo-petrol", turbo=True, power=120, torque=170, gearbox="AMT", speeds="6-speed",
         mileage=17.44, img=IMG + "6a745c35a7b66.jpg",
         sunroof=True, sunroof_price=9.79, sunroof_variant="Pure+ S AMT"),
    dict(name="Mahindra XUV 3XO", variant="MX2 Pro AT", price=9.99, body="Compact SUV", seats=5,
         engine="1.2L turbo-petrol", turbo=True, power=110, torque=200, gearbox="Automatic (TC)", speeds="6-speed",
         mileage=18.89, img=IMG + "6a745df8d8f8f.jpg",
         sunroof=True, sunroof_price=9.99, sunroof_variant="MX2 Pro AT"),
    # --- Added: automatics under ₹10 L whose cheapest automatic with a sunroof was listed by Autocar India.
    # Base automatic price not checked, so `price` = sunroof variant. No image / mileage available.
    dict(name="Tata Punch", variant="Pure+ S AMT", price=7.89, body="Compact SUV", seats=5,
         engine="1.2L petrol", turbo=False, power=88, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=None, img=None,
         sunroof=True, sunroof_price=7.89, sunroof_variant="Pure+ S AMT", base_known=False),
    dict(name="Hyundai Exter", variant="HX4+ AMT", price=8.06, body="Compact SUV", seats=5,
         engine="1.2L petrol", turbo=False, power=83, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=None, img=None,
         sunroof=True, sunroof_price=8.06, sunroof_variant="HX4+ AMT", base_known=False),
    dict(name="Skoda Kylaq", variant="Classic+ AT", price=9.25, body="Compact SUV", seats=5,
         engine="1.0L turbo-petrol", turbo=True, power=115, torque=None, gearbox="Automatic (TC)", speeds="Torque converter",
         mileage=None, img=None,
         sunroof=True, sunroof_price=9.25, sunroof_variant="Classic+ AT", base_known=False),
    dict(name="Maruti Dzire", variant="ZXi+ AMT", price=9.31, body="Sedan", seats=5,
         engine="1.2L petrol", turbo=False, power=82, torque=None, gearbox="AMT", speeds="5-speed",
         mileage=None, img=None,
         sunroof=True, sunroof_price=9.31, sunroof_variant="ZXi+ AMT", base_known=False),
    dict(name="Kia Sonet", variant="HTK(O) 1.0 Turbo DCT", price=9.89, body="Compact SUV", seats=5,
         engine="1.0L turbo-petrol", turbo=True, power=120, torque=None, gearbox="DCT", speeds="7-speed",
         mileage=None, img=None,
         sunroof=True, sunroof_price=9.89, sunroof_variant="HTK(O) DCT", base_known=False),
]

df = pd.DataFrame(CARS)
df["base_known"] = df["base_known"].fillna(True).astype(bool)
df["sunroof_extra"] = (df.sunroof_price - df.price).where(df.base_known)  # extra cost of sunroof over cheapest auto

# ------------------------------------------------------------------ SIDEBAR FILTERS
st.sidebar.header("🔎 Filters")

search = st.sidebar.text_input("Search by name", placeholder="e.g. Swift")

sunroof_choice = st.sidebar.radio(
    "☀️ Sunroof", ["Any", "With sunroof", "Without sunroof"],
    help="'With sunroof' shows the price of the cheapest AUTOMATIC variant that has one, "
         "and applies the budget slider to that price.")

with_sr = sunroof_choice == "With sunroof"
df["shown_price"] = df.sunroof_price.where(with_sr & df.sunroof, df.price)

budget = st.sidebar.slider("Ex-showroom price (₹ lakh)", 4.5, 10.0, (4.5, 10.0), step=0.25)

body_types = st.sidebar.multiselect("Body type", sorted(df.body.unique()), default=sorted(df.body.unique()))
gearboxes = st.sidebar.multiselect("Transmission", sorted(df.gearbox.unique()), default=sorted(df.gearbox.unique()))
seats = st.sidebar.radio("Seating", ["Any", "5", "7"], horizontal=True)
engine_type = st.sidebar.radio("Engine", ["Any", "Turbo only", "Naturally aspirated only"])

min_mileage = st.sidebar.slider("Min claimed mileage (kmpl)", 0, 30, 0)
min_power = st.sidebar.slider("Min power (PS/hp)", 0, 130, 0, step=5)
st.sidebar.caption("Mileage/power filters hide cars whose figures aren't listed.")

sort_by = st.sidebar.selectbox("Sort by", [
    "Price (low → high)", "Price (high → low)", "Mileage (high → low)",
    "Power (high → low)", "Sunroof extra cost (low → high)"])

# ------------------------------------------------------------------ APPLY FILTERS
f = df.copy()
if search:
    f = f[f.name.str.contains(search, case=False)]
if sunroof_choice == "With sunroof":
    f = f[f.sunroof]
elif sunroof_choice == "Without sunroof":
    f = f[~f.sunroof]
f = f[f.shown_price.between(*budget)]
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
    "Price (low → high)": ("shown_price", True),
    "Price (high → low)": ("shown_price", False),
    "Mileage (high → low)": ("mileage", False),
    "Power (high → low)": ("power", False),
    "Sunroof extra cost (low → high)": ("sunroof_extra", True),
}
col, asc = sorters[sort_by]
f = f.sort_values(col, ascending=asc, na_position="last").reset_index(drop=True)

# ------------------------------------------------------------------ HEADER
st.title("🚗 Petrol Automatic Cars Under ₹10 Lakh")
st.caption("Ex-showroom Delhi prices. On-road price in your city will be ~10–15% higher. "
           "Sources: CarDekho (Aug 2026) for base prices, Autocar India (Mar 2026) for sunroof variant prices.")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cars matching", len(f))
if len(f):
    m2.metric("Cheapest" + (" (sunroof)" if with_sr else ""), f"₹{f.shown_price.min():.2f} L")
    best = f.mileage.max()
    m3.metric("Best mileage", f"{best:.1f} kmpl" if pd.notna(best) else "—")
    m4.metric("With sunroof", int(f.sunroof.sum()))

if f.empty:
    st.warning("No cars match these filters. Try loosening them.")
    st.stop()


def fmt(v, suffix=""):
    return "—" if pd.isna(v) else f"{v:g}{suffix}"


def sunroof_line(r):
    if not r.sunroof:
        return "🚫 **Sunroof:** not offered (in automatic variants under ₹10 L)"
    extra = ""
    if pd.notna(r.sunroof_extra):
        extra = f" (+₹{r.sunroof_extra:.2f} L)" if r.sunroof_extra > 0 else " (no extra cost)"
    return f"☀️ **Sunroof:** {r.sunroof_variant} at ₹{r.sunroof_price:.2f} L{extra}"


tab_cards, tab_table, tab_compare, tab_chart = st.tabs(["🖼️ Cards", "📋 Table", "⚖️ Compare", "📊 Chart"])

# ------------------------------------------------------------------ CARDS
with tab_cards:
    cols = st.columns(3)
    for i, r in f.iterrows():
        with cols[i % 3].container(border=True):
            if isinstance(r.img, str):
                try:
                    st.image(r.img, use_container_width=True)
                except Exception:
                    st.write("🖼️ Image unavailable")
            else:
                st.write("🖼️ No image")
            st.subheader(r["name"])
            variant = r.sunroof_variant if (with_sr and r.sunroof) else r.variant
            st.caption(f"{variant} · {r.body} · {r.seats} seats")
            st.markdown(f"### ₹{r.shown_price:.2f} L")
            if r.sunroof:
                st.success(sunroof_line(r).replace("**", ""), icon="☀️")
            else:
                st.info("No sunroof in automatic variants under ₹10 L", icon="🚫")
            st.markdown(
                f"- **Engine:** {r.engine}\n"
                f"- **Power / Torque:** {fmt(r.power, ' PS')} / {fmt(r.torque, ' Nm')}\n"
                f"- **Gearbox:** {r.speeds} {r.gearbox}\n"
                f"- **Mileage:** {fmt(r.mileage, ' kmpl')}"
            )
            if not r.base_known:
                st.caption("Price shown is the sunroof variant; cheapest automatic variant not checked.")

# ------------------------------------------------------------------ TABLE
with tab_table:
    table = pd.DataFrame({
        "Car": f.name,
        "Variant": f.variant,
        "Body": f.body,
        "Seats": f.seats,
        "Cheapest auto (₹ L)": f.price,
        "Sunroof": f.sunroof.map({True: "Yes", False: "No"}),
        "Sunroof variant": f.sunroof_variant.fillna("—"),
        "Sunroof auto price (₹ L)": f.sunroof_price,
        "Sunroof extra (₹ L)": f.sunroof_extra.round(2),
        "Engine": f.engine,
        "Power (PS/hp)": f.power,
        "Torque (Nm)": f.torque,
        "Gearbox": f.speeds + " " + f.gearbox,
        "Mileage (kmpl)": f.mileage,
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download CSV", table.to_csv(index=False), "cars_under_10_lakh.csv", "text/csv")

# ------------------------------------------------------------------ COMPARE
with tab_compare:
    picks = st.multiselect("Pick 2–3 cars to compare", f.name.tolist(), max_selections=3)
    if len(picks) >= 2:
        sel = f[f.name.isin(picks)].set_index("name")
        cmp = pd.DataFrame({
            "Variant": sel.variant,
            "Cheapest auto (₹ L)": sel.price.map("{:.2f}".format),
            "Sunroof": sel.sunroof.map({True: "Yes", False: "No"}),
            "Sunroof variant": sel.sunroof_variant.fillna("—"),
            "Sunroof auto price (₹ L)": sel.sunroof_price.map(lambda v: "—" if pd.isna(v) else f"{v:.2f}"),
            "Body": sel.body,
            "Seats": sel.seats,
            "Engine": sel.engine,
            "Power (PS/hp)": sel.power.map(fmt),
            "Torque (Nm)": sel.torque.map(fmt),
            "Gearbox": sel.speeds + " " + sel.gearbox,
            "Mileage (kmpl)": sel.mileage.map(fmt),
        }).T
        st.dataframe(cmp, use_container_width=True)
    else:
        st.info("Select at least two cars.")

# ------------------------------------------------------------------ CHART
with tab_chart:
    metrics = {
        "Price shown (₹ L)": "shown_price",
        "Cheapest automatic price (₹ L)": "price",
        "Sunroof automatic price (₹ L)": "sunroof_price",
        "Sunroof extra cost (₹ L)": "sunroof_extra",
        "Mileage (kmpl)": "mileage",
        "Power": "power",
        "Torque (Nm)": "torque",
    }
    label = st.selectbox("Metric", list(metrics))
    chart_df = f.set_index("name")[metrics[label]].dropna()
    if chart_df.empty:
        st.info("No data for this metric in the current selection.")
    else:
        st.bar_chart(chart_df)

st.caption("Specs and prices vary by variant, city and time. Confirm final price, features and sunroof availability with your dealer.")
