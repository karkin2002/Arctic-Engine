from math import gcd

def find_common_ratios(current_values: tuple[int, int]) -> dict[float, tuple[int, int]]:
    g = gcd(current_values[0], current_values[1])
    simplified_value_1 = current_values[0] // g
    simplified_value_2 = current_values[1] // g
    
    common_ratios_dict = {}

    n = 1
    while True:
        x = simplified_value_1 * n
        y = simplified_value_2 * n
        if x > current_values[0] or y > current_values[1]:
            break
        scale = current_values[0] / x
        common_ratios_dict[scale] = (x, y)  # Use tuple for each result
        n += 1
        
    return common_ratios_dict

# Example usage
test = find_common_ratios((1920, 1080))
for i in test:
    print(i, test[i])