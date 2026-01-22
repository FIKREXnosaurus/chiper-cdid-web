# Database Mobil CTC-36
CARS = {
    "FTV": [57, 105, 162, 179],
    "A91": [45, 89, 133, 177, 221],
    "D56": [50, 79, 105, 121, 176],
    "N15": [58, 88, 118, 148, 178, 180]
}

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MODULO = 36

def clean_text(text):
    return text.replace(" ", "").upper()