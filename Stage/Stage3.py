from Object.Platform import Platform
from Object.Box import Box
from Char.Enemy import Enemy
from Char.Boss import Boss

class Stage3:
    name = "Stage 3 - Dark Castle"
    description = "Rintangan vertikal yang presisi, musuh patroli lebih ketat!"

    
    def create_map():
        platforms = [
            Platform(0, 650, 1500, 70),       
            Platform(1800, 650, 2000, 70),     
            Platform(4000, 650, 1500, 70),     
           
            Platform(400, 500, 150, 20),
            Platform(600, 400, 150, 20),
            Platform(900, 350, 250, 20),
            Platform(1400, 450, 200, 20),     
            Platform(1650, 350, 200, 20),      
            
            Platform(2100, 500, 300, 20),
            Platform(2500, 400, 300, 20),
            Platform(3000, 500, 400, 20),
        ]

        boxes = [
            Box(300, 600),
            Box(1000, 300),  
            Box(2200, 600),
            Box(2240, 600),  
            Box(3200, 450),
        ]

        enemies = [
            Enemy(500, 580),
            Enemy(950, 280),   
            Enemy(1900, 580),
            Enemy(2300, 580),
            Enemy(2600, 330),  
            Enemy(3100, 430),
            Enemy(3500, 580),
            Enemy(4200, 580),
        ]

         
        boss = Boss(5000, 580, 120) 

        return platforms, boxes, enemies, boss
