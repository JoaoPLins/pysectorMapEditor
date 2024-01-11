import csv
import tkinter as tk
from tkinter import Scrollbar
from tkinter import filedialog
from tkinter import simpledialog
tile_y = None
tile_x = None

def create_button(frame, text, command):
    button = tk.Button(frame, text=text, command=command)
    button.pack(side=tk.LEFT, padx=5, pady=5)
    return button

def draw_tile(canvas, x, y, tile_type):
    tile_size = 20
    x1 = x * tile_size
    y1 = y * tile_size
    x2 = x1 + tile_size
    y2 = y1 + tile_size
    color = "gray" if tile_type == "0" else "green"
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=tile_type)
    

def save_as(canvas, map_size, tile_size):
    # Open a file dialog to get the file name and location
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if not filepath:
        return  # The user cancelled; exit the function

    # Save the current map state to the selected file
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(map_array)
#        for y in range(map_size):
#            row = []
#            for x in range(map_size):
#                tile = get_tile_value(canvas, x, y, tile_size)
#                row.append(tile)
#            writer.writerow(row)

    # Update the current file name
    global current_filename
    current_filename = filepath

def save(canvas, tile_size):
    global current_filename
    if not current_filename:
        save_as(canvas, tile_size)  # If no file name is set, use Save As instead
        return

    # Determine the map size
  

    # Save the current map state to the existing file
    with open(current_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(map_array)


def undo():
    # Implement undo functionality
    pass

def redo():
    # Implement redo functionality
    pass

def zoom_in():
    # Implement zoom in functionality
    pass

def zoom_out():
    # Implement zoom out functionality
    pass

def tile_clicked(tile_id):
    # Logic when a tile is clicked
    # Update the label and entry box with the tile's information
    pass


def create_scrollable_canvas(root):
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Adding horizontal and vertical scrollbars
    h_scroll = Scrollbar(frame, orient=tk.HORIZONTAL)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    v_scroll = Scrollbar(frame)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    canvas = tk.Canvas(frame, bg="white",scrollregion=(0, 0, 4000, 4000),xscrollcommand=h_scroll.set,yscrollcommand=v_scroll.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    return canvas

def load_map(canvas, filename):
    tile_size = 20  # size of each tile is 20x20
    global global_map_size, map_array

    with open(filename, newline='') as csvfile:
        map_reader = csv.reader(csvfile, delimiter=',')
        map_array = list(map_reader)

    # Update global_map_size based on the loaded map
    global_map_size = len(map_array)

    # Clear the canvas before drawing the new map
    canvas.delete("all")

    # Draw the loaded map
    for y, row in enumerate(map_array):
        for x, tile_type in enumerate(row):
            draw_tile(canvas, x, y, tile_type)


def new_map(canvas, map_size):
    # Create a new map filled with zeros
    global global_map_size , map_array
    new_map_data = [["0" for _ in range(map_size)] for _ in range(map_size)]
    map_array = [["0" for _ in range(map_size)] for _ in range(map_size)]
    save_as(canvas,map_size, 20)
    # Clear the canvas
    canvas.delete("all")
    global_map_size = map_size
    
    for y in range(map_size):
        for x in range(map_size):
            draw_tile(canvas, x, y, "0")
            canvas.pack()

def get_tile_value(canvas, x, y, tile_size):
    x1 = x * tile_size
    y1 = y * tile_size
    x2 = x1 + tile_size
    y2 = y1 + tile_size

    # Find all text items in the area of the tile
    text_items = canvas.find_overlapping(x1, y1, x2, y2)

    for item in text_items:
        if canvas.type(item) == "text":
            # Assuming the text item is the value of the tile
            return canvas.itemcget(item, "text")

    # If no text item is found, return a default value (e.g., "0")
    return "0"

def highlight_tile(canvas, tile_x, tile_y, tile_size):
    # Remove previous highlight
    canvas.delete("highlight")

    x1 = tile_x * tile_size
    y1 = tile_y * tile_size
    x2 = x1 + tile_size
    y2 = y1 + tile_size

    canvas.create_rectangle(x1, y1, x2, y2, outline="blue", tags="highlight", width=2)



def select_tile(canvas, x, y, tile_size):
    global selected_tile_info
    global tile_x , tile_y
    global tile_value_entry

    tile_x = x // tile_size
    tile_y = y // tile_size

    selected_tile_info = (tile_x, tile_y)
    highlight_tile(canvas, tile_x, tile_y, tile_size)

    global selected_tile_label
    global tile_value
    global map_array
    
    tile_value = get_tile_value(canvas, tile_x, tile_y, tile_size)
    current_entry_value = tile_value_entry.get()
    if selected_tile_info is not None:
        previous_tile_x, previous_tile_y = selected_tile_info
        map_array[tile_x][tile_y] = current_entry_value
        draw_tile(canvas, previous_tile_x, previous_tile_y, current_entry_value)
        
    tile_value = get_tile_value(canvas, tile_x, tile_y, tile_size)

    
    
    # Update any UI elements if needed, like an entry field for the tile value

selected_tile_label = None 


def main():
    root = tk.Tk()
    root.title("Game Map Editor")
    root.geometry("800x600")
    
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill= tk.X)
    
    canvas = create_scrollable_canvas(root)
    canvas.pack()
    

    def loadn_map():
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        canvas.delete("all")
        if file_path:
            load_map(canvas,file_path)
        else:
            pass
    
    def new_map_button():
        
        factor = simpledialog.askstring("map size", "Insert the map size:")
        intfact = int(factor)
        if intfact > 0:
            new_map(canvas,intfact)
    def save_as_button():
        save_as(canvas,global_map_size,20)
    def save_button():
        save(canvas,20)

    def on_canvas_click(event):
        x, y = event.x, event.y
        select_tile(canvas, x, y, 20)
        
        canvas.bind("<Button-1>", on_canvas_click)  # Bind left mouse click
        
        updatelable()
        

    def update_tile_value(new_value):
        global selected_tile_info

        if selected_tile_info is None:
            return  # No tile is selected

        tile_x, tile_y = selected_tile_info
        # Update the tile value on the canvas
        # You might need to find and update the text item for the tile

        # Redraw the tile with the new value
        draw_tile(canvas, tile_x, tile_y, 20, new_value)

    

    canvas.bind("<Button-1>", on_canvas_click)
    global tile_y,tile_x
    create_button(top_frame,"New map", new_map_button)
    create_button(top_frame,"Load map", loadn_map)
    create_button(top_frame, "save as", save_as_button)
    create_button(top_frame, "Save", save_button)

    global tile_value_entry
    tile_value_entry = tk.Entry(top_frame,)
    tile_value_entry.insert(0, "0")
    tile_value_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    
    

    def updatelable():
        global selected_tile_label , tile_x, tile_y
        if selected_tile_label is not None:
            selected_tile_label.destroy()

        selected_tile_label = tk.Label(top_frame, text=f"Tile Selected: {tile_y} {tile_x}")
        selected_tile_label.pack(side=tk.LEFT, padx=5, pady=5)
        




    
    

    load_map(canvas, "map_data.csv")

    # Add more UI elements and functionalities here
    root.mainloop()

if __name__ == "__main__":
    main()
