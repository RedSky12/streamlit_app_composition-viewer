pip install streamlit plotly

import streamlit as st
import plotly.graph_objects as go

# ---------- 页面配置 ----------
st.set_page_config(page_title="构图对比分布图", layout="wide")
st.title("画面构成对比分析器")
st.caption("每个柱子代表一个对比维度，高度 1–10 表示对比强度。")

# ---------- 初始化 session state ----------
if "dims" not in st.session_state:
    st.session_state.dims = [
        {"name": "黑白对比", "value": 5},
        {"name": "明度对比", "value": 5},
        {"name": "大小对比", "value": 5},
    ]

MAX_DIMS = 7
MIN_DIMS = 1

# ---------- 工具函数 ----------
def add_dimension():
    if len(st.session_state.dims) < MAX_DIMS:
        st.session_state.dims.append({"name": f"维度{len(st.session_state.dims)+1}", "value": 5})

def remove_dimension(idx):
    if len(st.session_state.dims) > MIN_DIMS:
        del st.session_state.dims[idx]

# ---------- 控制栏 ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("编辑对比维度")
with col2:
    if st.button("➕ 添加维度", use_container_width=True):
        add_dimension()
        st.rerun()

# ---------- 每个维度的编辑行 ----------
for i, dim in enumerate(st.session_state.dims):
    cols = st.columns([2, 3, 0.8])
    with cols[0]:
        # 修改维度名称
        new_name = st.text_input(
            f"名称{i}",
            value=dim["name"],
            label_visibility="collapsed",
            key=f"name_{i}",
            placeholder="维度名称"
        )
        st.session_state.dims[i]["name"] = new_name
    with cols[1]:
        # 占比滑块 1-10
        new_val = st.slider(
            f"强度{i}",
            min_value=1,
            max_value=10,
            value=dim["value"],
            step=1,
            label_visibility="collapsed",
            key=f"val_{i}",
        )
        st.session_state.dims[i]["value"] = new_val
    with cols[2]:
        # 删除按钮（不能少于最小数量）
        if len(st.session_state.dims) > MIN_DIMS:
            if st.button("🗑️", key=f"del_{i}", use_container_width=True, help="删除此维度"):
                remove_dimension(i)
                st.rerun()
        else:
            st.write("")  # 占位

# ---------- 绘制柱形图 ----------
st.markdown("---")
fig = go.Figure()

names = [d["name"] for d in st.session_state.dims]
values = [d["value"] for d in st.session_state.dims]

fig.add_trace(go.Bar(
    x=names,
    y=values,
    text=values,
    textposition="outside",
    marker_color="#5DADE2",
    width=0.5,
))

# 固定竖轴 1-10，并且上下标注“强烈/不强烈”
fig.update_yaxes(
    range=[0.5, 10.5],  # 留出边距
    tickvals=list(range(1, 11)),
    title="← 弱 —————————— 强 →",
    title_standoff=0,
    gridcolor="lightgray",
)

fig.update_xaxes(
    title="对比维度",
    tickangle=0,
)

fig.update_layout(
    title="构图对比强度分布",
    height=500,
    margin=dict(t=40, b=40),
    plot_bgcolor="white",
)

st.plotly_chart(fig, use_container_width=True)

# ---------- 提示信息 ----------
st.caption(f"当前维度数量：{len(st.session_state.dims)} / {MAX_DIMS}")
