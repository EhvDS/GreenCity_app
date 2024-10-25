import streamlit as st
import json

# Load JSON data
with open("../data/youssef/json.json", "r") as file:
    data = json.load(file)
items = data["items"]

# Define the base directory for images
image_base_path = "../data/youssef/images/"

# Sidebar filters for Category and Target Group
st.sidebar.header("Filter Options")
available_categories = list(set([item["categories"] for item in items]))
available_target_groups = list(set([group for item in items if "Target group" in item for group in item["Target group"]]))

selected_category = st.sidebar.selectbox("Select Category", ["All"] + available_categories)
selected_target_group = st.sidebar.selectbox("Select Target Group", ["All"] + available_target_groups)

# Filter items based on selected category and target group
filtered_items = [
    item for item in items
    if (selected_category == "All" or item["categories"] == selected_category) and
       (selected_target_group == "All" or selected_target_group in item["Target group"])
]

# Display the items in a grid view
st.title("Ecological Projects Overview")

selected_item_name = None
cols = st.columns(3)
for i, item in enumerate(filtered_items):
    with cols[i % 3]:
        # Construct the full image path
        image_path = os.path.join(image_base_path, os.path.basename(item["image"]))
        if os.path.exists(image_path):  # Check if the image exists
            st.image(image_path, use_column_width=True)
        else:
            st.write("Image not available")
        if st.button(item["name"]):
            selected_item_name = item["name"]

# Show details for the selected item
if selected_item_name:
    selected_item = next(item for item in items if item["name"] == selected_item_name)
    st.header(selected_item["name"])

    # Sections
    st.subheader("Sections")
    for section in selected_item["sections"]:
        st.write(f"**{section['header']}**")
        st.write(section["text"])

    # Guidelines
    st.subheader("Guidelines")
    for guideline in selected_item["guidelines"]["options"]:
        st.write(f"**{guideline['title']}**")
        st.write(guideline["text"])