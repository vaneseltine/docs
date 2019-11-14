pandas
######

pd.crosstab()
--------------

Why do::

    diamonds_agg = diamonds.groupby(['cut', 'color']).size().reset_index()
    heatmap_df = pd.pivot_table(diamonds_agg, values=0, index=['cut'], columns='color')

when you can::

    heatmap_df = pd.crosstab(diamonds.cut, diamonds.color)
