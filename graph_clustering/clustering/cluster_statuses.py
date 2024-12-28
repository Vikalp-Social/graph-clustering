def cluster_statuses(statuses, parts, title_prefix="Part", dont_repeat=False, percent_element_to_repeat=50, percent_parts_to_repeat_in=50):

    """
    Splits a list into `n` parts and optionally repeats elements across parts based on specified percentages.

    Args:
        elements (list): The list to split.
        n (int): Number of parts to split into.
        title_prefix (str): Prefix for part titles.
        dont_repeat (bool): If True, parts will not repeat elements.
        percent_element_to_repeat (int): Percentage of elements in each part to repeat into others.
        percent_parts_to_repeat_in (int): Percentage of parts to include repeated elements.

    Returns:
        dict: A dictionary where keys are part titles and values are dictionaries with counts and elements.
    """

    if not statuses:
        return {}

    parts = min(parts, len(statuses))

    percent_element_to_repeat = min(percent_element_to_repeat, 100)

    percent_parts_to_repeat_in = min(percent_parts_to_repeat_in, 100)

    # Determine the size of each chunk
    k, m = divmod(len(statuses), parts)  # k: size of each chunk, m: remainder
    parts = [statuses[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts)]

    if not dont_repeat:

        overlap_size = round((percent_element_to_repeat / 100) * k)

        parts_to_repeat_in = round((percent_parts_to_repeat_in / 100) * parts)

        for i in range(parts_to_repeat_in):
            for j in range(parts_to_repeat_in):
                if i == j:
                    continue
                overlap_elements = parts[j][:overlap_size]
                parts[i].extend(overlap_elements)


    # Create the dictionary with titles
    result = {f"{title_prefix} {i + 1}": {"count": len(part), "elements": part} for i, part in enumerate(parts)}

    return result

# # Example usage
# elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# n = 3
# output = split_list_to_dict(elements, n)
# print(output)
