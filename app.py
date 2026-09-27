import streamlit as st

st.set_page_config(
    page_title="Second Life AI",
    page_icon="♻️"
)

# ---------------- PROJECT DATABASE ----------------

projects = {
    "jeans": {
        "name": "Denim Storage Pouch",
        "description": "Old jeans nu useful storage pouch vich transform karo.",
        "materials": ["Old jeans", "Scissors", "Thread or fabric glue"],
        "advantages": [
            "Old jeans reuse hundi aa",
            "Small items store kar sakde ho",
            "New storage product khareedan di need ghatt hundi aa"
        ],
        "steps": [
            "Jeans da pocket section carefully cut karo.",
            "Pocket de around thoda denim border rakho.",
            "Thread naal stitch karo ya suitable fabric adhesive use karo.",
            "Hun isnu small items store karan layi use karo."
        ]
    },

    "bottle": {
        "name": "Plastic Bottle Mini Planter",
        "description": "Old plastic bottle nu mini plant pot vich transform karo.",
        "materials": ["Clean plastic bottle", "Scissors", "Soil", "Small plant"],
        "advantages": [
            "Plastic bottle reuse hundi aa",
            "Low-cost planter ban janda aa",
            "Bottle nu waste hon ton bachaya janda aa"
        ],
        "steps": [
            "Bottle nu clean te dry karo.",
            "Adult di help naal bottle nu required height te cut karo.",
            "Suitable drainage holes banao.",
            "Soil te small plant add karo."
        ]
    },

    "tshirt": {
        "name": "Old T-Shirt Tote Bag",
        "description": "Old T-shirt nu reusable carry bag vich transform karo.",
        "materials": ["Old T-shirt", "Scissors", "Thread or fabric glue"],
        "advantages": [
            "Old clothing reuse hundi aa",
            "Reusable bag ban janda aa",
            "Lightweight items carry kar sakde ho"
        ],
        "steps": [
            "T-shirt nu flat rakho.",
            "Sleeves cut karo.",
            "Bottom side nu stitch karo.",
            "T-shirt nu turn karke reusable bag banao."
        ]
    },

    "cardboard": {
        "name": "Cardboard Phone Stand",
        "description": "Old cardboard box nu phone stand vich transform karo.",
        "materials": ["Cardboard", "Scissors", "Glue or paper tape"],
        "advantages": [
            "Old cardboard reuse hunda aa",
            "Phone nu upright rakh sakda hai",
            "New phone stand khareedan di need nahi"
        ],
        "steps": [
            "Cardboard de required pieces cut karo.",
            "Phone support karan layi front lip banao.",
            "Pieces nu glue, tape ya cardboard tabs naal join karo.",
            "Flat surface te stand test karo."
        ]
    },

    "paper": {
        "name": "Recycled Paper Gift Box",
        "description": "Old paper/card sheets nu small reusable gift box vich transform karo.",
        "materials": ["Old paper or card", "Scissors", "Paper glue"],
        "advantages": [
            "Old paper reuse hunda aa",
            "Small gifts store kar sakde ho",
            "Simple decorative product ban janda aa"
        ],
        "steps": [
            "Paper nu square shape vich cut karo.",
            "Fold lines banao.",
            "Sides nu fold karke box shape banao.",
            "Edges nu glue naal secure karo."
        ]
    }
}


# ---------------- AI MATERIAL DETECTION ----------------

def find_project(user_text):

    text = user_text.lower()

    # Jeans / denim
    if any(word in text for word in [
        "jeans", "denim", "old pants", "trouser", "pants"
    ]):
        return projects["jeans"]

    # Plastic bottle
    if any(word in text for word in [
        "plastic bottle", "water bottle", "bottle", "pet bottle"
    ]):
        return projects["bottle"]

    # T-shirt
    if any(word in text for word in [
        "t-shirt", "tshirt", "t shirt", "old shirt", "tee shirt"
    ]):
        return projects["tshirt"]

    # Cardboard
    if any(word in text for word in [
        "cardboard", "cardboard box", "old box", "carton", "box"
    ]):
        return projects["cardboard"]

    # Paper
    if any(word in text for word in [
        "paper", "old paper", "newspaper", "card sheet"
    ]):
        return projects["paper"]

    return None


# ---------------- APP UI ----------------

st.title("♻️ SECOND LIFE AI")

st.subheader("Don't throw it. Transform it.")

st.write(
    "AI nu dasso tuhade kol ki old material/object aa. "
    "AI tuhanu ik useful new product suggest karega."
)

material = st.text_area(
    "📦 What do you have?",
    placeholder="Example: old jeans"
)

goal = st.text_input(
    "🎯 What do you want to make?",
    placeholder="Example: something useful"
)


if st.button("✨ ASK AI", use_container_width=True):

    if material.strip() == "":
        st.warning("Please enter a material first.")

    else:

        result = find_project(material)

        if result is None:

            st.info(
                "🤖 AI nu is material da exact project nahi milia. "
                "Try: old jeans, plastic bottle, old T-shirt, cardboard box, or old paper."
            )

        else:

            st.success("🤖 AI found a reuse idea!")

            st.markdown("---")

            st.header(result["name"])

            st.write(result["description"])

            # ---------------- MATERIALS ----------------

            st.subheader("🧰 Materials Needed")

            for item in result["materials"]:
                st.write("•", item)

            # ---------------- ADVANTAGES ----------------

            st.subheader("🌱 Advantages")

            for advantage in result["advantages"]:
                st.write("•", advantage)

            # ---------------- STEPS ----------------

            st.subheader("🪜 How To Make It")

            for number, step in enumerate(result["steps"], 1):
                st.write(f"**{number}.** {step}")

            # ---------------- CHATBOT ----------------

            st.markdown("---")

            st.subheader("💬 Missing a material? Ask AI")

            missing = st.text_input(
                "What material are you missing?",
                placeholder="Example: I don't have glue"
            )

            if missing:

                missing_text = missing.lower()

                if "glue" in missing_text:

                    st.info(
                        "🤖 AI: You can use suitable tape or folded cardboard "
                        "tabs where appropriate. For fabric projects, stitching "
                        "can be used instead of fabric glue. Ask an adult for help "
                        "if sewing or cutting is needed."
                    )

                elif "scissors" in missing_text:

                    st.info(
                        "🤖 AI: Don't use unsafe substitutes. Ask an adult "
                        "for help getting suitable scissors."
                    )

                elif "thread" in missing_text:

                    st.info(
                        "🤖 AI: For fabric projects, suitable fabric adhesive "
                        "may work as an alternative. Follow the product instructions."
                    )

                else:

                    st.info(
                        "🤖 AI: I don't have a tested replacement for that "
                        "material. It's safer to use the listed materials."
                    )


# ---------------- AI ETHICS ----------------

st.markdown("---")

st.caption(
    "🔐 AI Ethics: This prototype only uses the material information "
    "you enter. It does not ask for your name, address, or other personal data."
)