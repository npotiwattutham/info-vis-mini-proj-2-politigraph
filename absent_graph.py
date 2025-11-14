import base64
import requests

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Helper function for clipping the image into circle
def make_circular_image(url, diameter):
    """
    Convert an image URL into a circular SVG image (base64-encoded)
    and return a data URL suitable for Plotly layout.images.
    """
    # Load image data
    img_data = requests.get(url).content
    img_b64 = base64.b64encode(img_data).decode("utf-8")

    # Create circular SVG wrapper
    svg_template = f"""
    <svg width="{diameter}" height="{diameter}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <clipPath id="circleView">
                <circle cx="{diameter/2}" cy="{diameter/2}" r="{diameter/2}" />
            </clipPath>
        </defs>
        <image href="data:image/jpeg;base64,{img_b64}"
               width="{diameter}" height="{diameter}" clip-path="url(#circleView)" />
    </svg>
    """

    svg_b64 = base64.b64encode(svg_template.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{svg_b64}"

class BubbleChartPlotly:
    def __init__(self, labels, area, image_urls, bubble_spacing=10, plot_diameter=500):
        self.labels = labels
        self.image_urls = image_urls
        self.area = np.asarray(area)
        self.plot_diameter = plot_diameter
        self.plot_radius = plot_diameter / 2.5
        self.bubble_spacing = bubble_spacing

        total_area = np.sum(self.area)
        max_allowed_area = (np.pi * (self.plot_radius ** 2)) * 0.6
        scale_factor = max_allowed_area / total_area
        self.scaled_area = self.area * scale_factor
        self.radii = np.sqrt(self.scaled_area / np.pi)

        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = self.radii
        self.bubbles[:, 3] = self.scaled_area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3])

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0], bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        return self.center_distance(bubble, bubbles) - bubble[2] - bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return np.argmin(distance, keepdims=True)

    def collapse(self, n_iterations=100):
        for _ in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                dir_vec = self.com - self.bubbles[i, :2]
                norm = np.linalg.norm(dir_vec)
                if norm == 0:
                    continue
                dir_vec = dir_vec / norm

                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        norm = np.linalg.norm(dir_vec)
                        if norm == 0:
                            continue
                        dir_vec = dir_vec / norm
                        orth = np.array([dir_vec[1], -dir_vec[0]])

                        new_point1 = self.bubbles[i, :2] + orth * self.step_dist
                        new_point2 = self.bubbles[i, :2] - orth * self.step_dist

                        dist1 = self.center_distance(self.com, np.array([new_point1]))
                        dist2 = self.center_distance(self.com, np.array([new_point2]))

                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.05:
                self.step_dist /= 2

    def to_dataframe(self):
        return pd.DataFrame({
            'x': self.bubbles[:, 0],
            'y': self.bubbles[:, 1],
            'radius': self.bubbles[:, 2],
            'size': self.bubbles[:, 3],
            'label': self.labels,
            'image_url': self.image_urls
        })

def plot_bubble_chart_with_images(df, plot_diameter=500):
    chart = BubbleChartPlotly(
        labels=df["label"],
        area=df["size"],
        image_urls=df["image_url"],
        bubble_spacing=1,
        plot_diameter=plot_diameter
    )

    chart.collapse()
    df_bubbles = chart.to_dataframe()

    fig = go.Figure()

    # Invisible marker for interaction
    fig.add_trace(go.Scatter(
        x=df_bubbles["x"],
        y=df_bubbles["y"],
        mode="markers",
        marker=dict(size=df_bubbles["radius"] * 2, opacity=0),
        text=df_bubbles["label"],
        textposition="middle center",
        hovertemplate="<b>%{text}</b><extra>%{text}</extra>"
    ))

    # Add images as bubbles
    for i, row in df_bubbles.iterrows():
        r = row["radius"]
        diameter = int(2 * r)

        svg_url = make_circular_image(row["image_url"], diameter)

        fig.add_layout_image(
            dict(
                source=svg_url,
                x=row["x"] - r,
                y=row["y"] + r,
                sizex=diameter,
                sizey=diameter,
                xref="x",
                yref="y",
                layer="above",
                sizing="stretch",
            )
        )

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        width=plot_diameter,
        height=plot_diameter,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig
    
    
def absent_graph():
    df = pd.read_pickle('./ABSENT_RATIO.pkl')
    df['image_url'] = df['image_url'].fillna('https://www.gravatar.com/avatar/?d=mp&s=200')
    return plot_bubble_chart_with_images(df[:100], plot_diameter=600)