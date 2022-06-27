from pandas import read_csv
import pandas as pd

class ActionData:
    properties = []
    selection = 0
    
    def change_display(self):
        properties = self.properties
        selection = self.selection
        _ = properties[selection]
        display_message = f"""
                            为您找到 {len(properties)} 条食谱，当前显示第 {selection+1} 条

                            食谱名称：{_.Dishes}
                            荤菜部分：{_.Meat       if not pd.isna(_.Meat)       else ""}
                            素菜部分：{_.Vegetarian if not pd.isna(_.Vegetarian) else ""}
                            主食部分：{_.Staple     if not pd.isna(_.Staple)     else ""}
                            烹饪工具：{_.Tool       if not pd.isna(_.Tool)       else ""}
                            教学视频：{_.Tutorial   if not pd.isna(_.Tutorial)   else ""}
                            """
        return display_message

    def goto_next_property(self):
        # WHEN CHANGED
        if self.selection < len(self.properties)-1:
            self.selection += 1
        return self.change_display()

    def goto_prev_property(self):
        if self.selection > 0:
            self.selection -= 1
        return self.change_display()