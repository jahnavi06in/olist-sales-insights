def page_satisfaction() -> None:
    if not (HAS_REVIEW and HAS_LATE):
        st.info("Review scores not found. Add data/olist_order_reviews_dataset.csv to the data folder.")
        return

    rev = orders_df.dropna(subset=["review_score"]).copy()
    if rev.empty:
        st.info("No review data under the current filters.")
        return

    on_time_mask = rev["is_late"] == 0
    late_mask = rev["is_late"] == 1
    avg_all = rev["review_score"].mean()
    avg_on_time = rev.loc[on_time_mask, "review_score"].mean()
    avg_late = rev.loc[late_mask, "review_score"].mean()
    low_on_time = (rev.loc[on_time_mask, "review_score"] <= 2).mean() * 100
    low_late = (rev.loc[late_mask, "review_score"] <= 2).mean() * 100

    a, b, c = st.columns(3)
    with a:
        insight_card("⭐", "Average review score", value=f"{avg_all:.2f} / 5",
                     description=f"{len(rev):,} reviewed orders")
    with b:
        insight_card("✅", "On-time orders", value=f"{avg_on_time:.2f} / 5",
                     description=f"{low_on_time:.1f}% rated 1-2 stars")
    with c:
        insight_card("⏰", "Late orders", value=f"{avg_late:.2f} / 5" if pd.notna(avg_late) else "N/A",
                     description=f"{low_late:.1f}% rated 1-2 stars" if pd.notna(low_late) else "")

    if pd.notna(avg_late) and pd.notna(avg_on_time):
        gap = avg_on_time - avg_late
        decision_card(
            "Delivery impact on satisfaction",
            f"Late deliveries score {gap:.2f} points lower than on-time deliveries",
            f"{low_late:.1f}% of late orders get 1-2 stars versus {low_on_time:.1f}% of on-time orders. "
            "Reducing late deliveries is a direct lever for customer satisfaction and repeat purchases.",
        )

    c1, c2 = st.columns(2)
    with c1:
        with card("sat-bucket"):
            card_head("📦", "Review score by delivery time", "Average score per delivery-time bucket")
            labels = ["0-7 days", "8-14 days", "15-21 days", "22-30 days", "31+ days"]
            rev["bucket"] = pd.cut(
                rev["delivery_days"], bins=[-1, 7, 14, 21, 30, 10_000], labels=labels
            )
            bucket = rev.groupby("bucket", observed=True)["review_score"].mean().reset_index()
            fig = px.bar(bucket, x="bucket", y="review_score", color="review_score",
                         color_continuous_scale=["#FEE2E2", "#F59E0B", "#10B981"])
            style_fig(fig, 380)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(title="")
            fig.update_yaxes(title="Avg review score", range=[1, 5])
            show_chart(fig)
    with c2:
        with card("sat-dist"):
            card_head("📊", "Score distribution", "Share of orders by star rating")
            rev["delivery"] = rev["is_late"].map({0: "On time", 1: "Late"})
            rev["stars"] = rev["review_score"].round().astype(int)
            dist = rev.groupby(["delivery", "stars"]).size().reset_index(name="n")
            dist["share"] = dist["n"] / dist.groupby("delivery")["n"].transform("sum") * 100
            fig = px.bar(dist, x="stars", y="share", color="delivery", barmode="group",
                         color_discrete_map={"On time": GREEN, "Late": RED})
            style_fig(fig, 380)
            fig.update_xaxes(title="Stars", dtick=1)
            fig.update_yaxes(title="% of orders", ticksuffix="%")
            show_chart(fig)
