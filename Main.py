import flet as ft

def main(page: ft.Page):
    page.title = "Diet Master Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.scroll = "auto"
    page.padding = 20

    height_field = ft.TextField(label="قد (سانتی‌متر)", prefix_icon=ft.icons.HEIGHT, keyboard_type=ft.KeyboardType.NUMBER)
    weight_field = ft.TextField(label="وزن فعلی (کیلوگرم)", prefix_icon=ft.icons.MONITOR_WEIGHT, keyboard_type=ft.KeyboardType.NUMBER)
    age_field = ft.TextField(label="سن", prefix_icon=ft.icons.CAKE, keyboard_type=ft.KeyboardType.NUMBER)
    
    gender_radio = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="agha", label="آقا (BMI 23)"),
        ft.Radio(value="khanom", label="خانم (BMI 22)")
    ], alignment=ft.MainAxisAlignment.CENTER))

    results_container = ft.Column(spacing=20)

    def calculate_diet(e):
        try:
            h = float(height_field.value) / 100
            w = float(weight_field.value)
            age = int(age_field.value)
            gender = gender_radio.value

            if not gender:
                page.snack_bar = ft.SnackBar(ft.Text("لطفاً جنسیت را انتخاب کنید"))
                page.snack_bar.open = True
                page.update()
                return

            bmi_target = 23 if gender == "agha" else 22
            ibw = bmi_target * (h ** 2)
            aibw = ((w - ibw) / 3) + ibw
            tdee = aibw * 1.1 * 1.3 * 24
            target_cal = max(tdee - 1000, 1200)

            cho_g = (target_cal * 0.53) / 4
            pro_g = (target_cal * 0.17) / 4
            fat_g = (target_cal * 0.30) / 9

            u_milk, u_veg = 2, 3
            u_fruit = 4 if target_cal > 1800 else (3 if target_cal > 1500 else 2)

            def get_units(cho, pro, fat, sugar_units=0):
                adj_cho = cho - (sugar_units * 5)
                bread = max(round((adj_cho - (u_milk * 12) - (u_veg * 5) - (u_fruit * 15)) / 15), 6)
                meat = max(round((pro - (u_milk * 8) - (u_veg * 2) - (bread * 2)) / 7), 2)
                fat_u = max(round((fat - (u_milk * 3) - (meat * 3)) / 5), 3)
                return bread, meat, fat_u

            b1, m1, f1 = get_units(cho_g, pro_g, fat_g, 0)
            u_sugar = max(round((target_cal * 0.05) / 20), 1)
            b2, m2, f2 = get_units(cho_g, pro_g, fat_g, u_sugar)

            results_container.controls.clear()
            results_container.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"کالری هدف: {int(target_cal)} kcal", size=20, weight="bold", color=ft.colors.GREEN),
                            ft.Text(f"وزن تعدیل شده: {round(aibw, 1)} kg", size=16),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20
                    )
                )
            )

            def create_diet_card(title, b, m, s, color):
                return ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(title, weight="bold", size=18, color=color),
                            ft.Divider(),
                            ft.Row([ft.Icon(ft.icons.BREAD_ASSET), ft.Text(f"نان و غلات: {b} واحد")]),
                            ft.Row([ft.Icon(ft.icons.EGG), ft.Text(f"گوشت و پروتئین: {m}")]),
                            ft.Row([ft.Icon(ft.icons.APPLE), ft.Text(f"میوه: {u_fruit} | لبنیات: {u_milk} | سبزی: {u_veg}")]),
                            ft.Row([ft.Icon(ft.icons.WATER_DROP), ft.Text(f"چربی: {f1} | قند ساده: {s}")]),
                        ])
                    )
                )

            results_container.controls.append(create_diet_card("رژیم استاندارد (بدون قند)", b1, m1, 0, ft.colors.BLUE))
            results_container.controls.append(create_diet_card("رژیم با قند ساده", b2, m2, u_sugar, ft.colors.ORANGE))
            
            page.update()

        except Exception as ex:
            print(ex)

    page.add(
        ft.Text("محاسبه‌گر رژیم", size=28, weight="bold", color=ft.colors.BLUE_800),
        height_field,
        weight_field,
        age_field,
        gender_radio,
        ft.ElevatedButton(
            "تولید برنامه رژیم",
            icon=ft.icons.CALCULATE,
            on_click=calculate_diet,
            height=50,
            width=400
        ),
        results_container
    )

ft.app(target=main)
