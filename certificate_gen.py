import os, shutil, sys
from tkinter import Tk, Frame, Label, PhotoImage, Entry, Button, messagebox, Menu, Toplevel, filedialog,ttk, simpledialog, colorchooser
import turtle
from PIL import Image, ImageDraw, ImageFont


class FileExplorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")
        self.root.geometry("800x600")

        self.icon_dir = os.path.dirname(os.path.abspath(__file__)) # Directory where the script is located

        self.frame_top = Frame(self.root)
        self.frame_top.pack(pady=10)

        self.download_button = Button(self.frame_top, text="Download All", command=self.download_files)
        self.download_button.config(
            bg="#5b98c7",
            fg="#ffffff",
            bd=0,
            padx=10,
            pady=5,
            activebackground="#0059b3",
            activeforeground="#ffffff"
        )
        self.download_button.pack(side="left", padx=10)

        self.entry = Entry(self.frame_top, width=50)
        self.entry.config(
            bg="#ffffff",  # Background color
            fg="#333333",  # Text color
            bd=1,  # Border width
            highlightthickness=2,  # Border thickness
            highlightbackground="#ffffff",  # Border color
            highlightcolor="#b6d4ea"  # Border color (when active)
        )
        self.entry.pack(side="left")

        self.button_new_folder = Button(self.frame_top, text="+ New Project", command=self.create_new_folder)
        self.button_new_folder.config(
            bg="#5b98c7",  # Background color
            fg="#ffffff",  # Text color
            bd=0,  # Border width
            padx=10,  # Horizontal padding
            pady=5,  # Vertical padding
            activebackground="#0059b3",  # Background color when active
            activeforeground="#ffffff"  # Text color when active
        )
        self.button_new_folder.pack(side="left", padx=10)

        self.button_back = Button(self.frame_top, text="< Back", command=self.navigate_back)
        self.button_back.pack(side="left", padx=10)

        self.frame = Frame(self.root)
        self.frame.pack(pady=20)

        self.path_history = [os.getcwd()]  # Initialize with the current directory

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Rename", command=self.rename_folder)
        self.context_menu.add_command(label="Delete", command=self.delete_folder)
        self.context_menu.add_command(label="Properties", command=self.view_properties)
        
        self.root.bind("<Button-3>", self.show_context_menu)

        self.refresh()
        

    
    def download_files(self):
        current_directory = self.path_history[-1]

        # Ask the user to select a destination directory
        destination_directory = filedialog.askdirectory(title="Select Destination Directory")

        if destination_directory:
            current_directory = self.path_history[-1]
            directories, files = self.get_files_and_directories()

            for directory in directories:
                try:
                    shutil.copytree(
                        os.path.join(current_directory, directory.name),
                        os.path.join(destination_directory, directory.name),
                        copy_function=shutil.copy2
                    )
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy directory:\n{str(e)}")

            for file in files:
                try:
                    shutil.copy2(
                        os.path.join(current_directory, file.name),
                        os.path.join(destination_directory, file.name)
                    )
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy file:\n{str(e)}")

            messagebox.showinfo("Success", "Files copied successfully.")

        self.refresh()

    def get_files_and_directories(self):
        current_directory = self.path_history[-1]
        items = os.scandir(current_directory)
        files = []
        directories = []

        for item in items:
            if item.is_file():
                files.append(item)
            else:
                directories.append(item)

        return directories, files

    def open_directory(self, directory):
        current_directory = self.path_history[-1]  # Get the current directory from history
        new_directory = os.path.join(current_directory, directory)  # Get the new directory path
        self.path_history.append(new_directory)  # Add the new directory to history
        self.refresh()

    def navigate_back(self):
        if len(self.path_history) > 1:  # Ensure at least one previous directory is available
            self.path_history.pop()  # Remove the current directory from history
            self.refresh()

    # def open_file(self, file):
    #     os.startfile(file.path)  # Open file with default 
    def open_file(self, file):
        file_name = os.path.basename(file.path)
        extension = os.path.splitext(file_name)[1].lower()

        #disabled_files = ['file_explorer_gui.py', 'readme.txt', 'folder_icon.png', 'file_icon.png', 'main.py', 'arial.ttf']
        disabled_files = []
        if file_name in disabled_files:
            try:
                with open(file.path, "r") as f:
                    file_content = f.read()

                messagebox.showinfo("File Content (Read-Only)", file_content, parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the file:\n{str(e)}")
        elif extension == ".png" or extension == ".txt":
            os.startfile(file.path)  # Open PNG file with default application
        
        else:
            messagebox.showwarning("Warning", "Unsupported file format.", parent=self.root)

    def create_new_folder(self):
        folder_name = self.entry.get().strip()
        current_directory = self.path_history[-1]  # Get the current directory from history

        if folder_name:
            try:
                new_folder_path = os.path.join(current_directory, folder_name)  # Create the full path for the new folder
                os.mkdir(new_folder_path)  # Create the new folder in the current directory
                
                # Open a new window for additional inputs
                self.open_additional_inputs(new_folder_path)

                self.refresh()
                self.entry.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create the folder:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a valid folder name.")

    def open_additional_inputs(self, folder_path):
        dialog = Toplevel(self.root)
        dialog.title("Additional Inputs")
        dialog.geometry("600x200")

        dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog)
        frame.pack(pady=10)

        label = ttk.Label(frame, text="Enter atleast one name:")
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        entry = ttk.Entry(frame, width=30)
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.insert(0, "names")  # Set default file name

        def select_png_file():
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            entry_file_path.delete(0, "end")
            entry_file_path.insert(0, file_path)

        label_file_path = ttk.Label(frame, text="Select PNG file:")
        label_file_path.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        entry_file_path = ttk.Entry(frame, width=30)
        entry_file_path.grid(row=1, column=1, padx=5, pady=5)

        button_select_file = ttk.Button(frame, text="Select", command=select_png_file)
        button_select_file.grid(row=1, column=2, padx=5, pady=5)

            
        label_width = ttk.Label(frame, text="Enter width (pixels):")
        label_width.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        entry_width = ttk.Entry(frame, width=10)
        entry_width.grid(row=2, column=1, padx=5, pady=5)
        entry_width.insert(0, "1056")  # Set default width

        label_height = ttk.Label(frame, text="Enter height (pixels):")
        label_height.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        entry_height = ttk.Entry(frame, width=10)
        entry_height.grid(row=3, column=1, padx=5, pady=5)
        entry_height.insert(0, "816")  # Set default height

        def save_inputs():
            file_name = entry.get().strip()
            png_file_path = entry_file_path.get().strip()
            width = entry_width.get().strip()
            height = entry_height.get().strip()

            if file_name and png_file_path and width and height:
                # Create a text file with the provided content
                text_file_path = os.path.join(folder_path, "names.txt")  # Set default file name
                with open(text_file_path, "w") as f:
                    f.write(file_name)

                image = Image.open(png_file_path)
                resized_image = image.resize((int(width), int(height)))

                # Copy the selected PNG file to the new project folder
                resized_image.save(os.path.join(folder_path, "sample.png"))  # Set default file name
                dialog.grab_release()  # Release the grab on the dialog
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a valid file name and select a PNG file.")

        button_save = ttk.Button(dialog, text="Save", command=save_inputs)
        button_save.pack(pady=10)

    def rename_folder(self):
        selected_folder = self.context_menu_path

        # Create a custom dialog box
        dialog = Toplevel(self.root)
        dialog.title("Rename Folder")
        dialog.geometry("300x100")

        label = Label(dialog, text="Enter new folder name:")
        label.pack()

        entry = Entry(dialog, width=30)
        entry.pack(pady=10)

        def rename():
            new_name = entry.get().strip()

            if new_name:
                try:
                    os.rename(selected_folder, new_name)
                    dialog.destroy()
                    self.refresh()
                except Exception as e:
                    dialog.destroy()
                    messagebox.showerror("Error", f"Failed to rename the folder:\n{str(e)}")
            else:
                messagebox.showwarning("Warning", "Please enter a valid folder name.")

        button_rename = Button(dialog, text="Rename", command=rename)
        button_rename.pack()

    def delete_folder(self):
        selected_folder = self.context_menu_path
        confirmation = messagebox.askyesno(
            "Delete Folder",
            f"Are you sure you want to delete the folder:\n{selected_folder}?\nThis action cannot be undone.",
            parent=self.root,
        )

        if confirmation:
            try:
                # Use shutil.rmtree() to remove the directory and its contents recursively
                shutil.rmtree(selected_folder)
                self.refresh()
            except Exception as e:
                print(selected_folder+".......")
                messagebox.showerror("Error", f"Failed to delete the folder:\n{str(e)}")


    def view_properties(self):
        selected_folder = self.context_menu_path
        properties = f"Folder Path: {selected_folder}"

        messagebox.showinfo("Folder Properties", properties, parent=self.root)

    def show_context_menu(self, event):
        widget = event.widget
        self.context_menu_path = widget.cget("text")

        # List of file names to disable the context menu for
        disabled_files = ['readme.txt','folder_icon.png', 'file_icon.png',"arial.ttf"]

        file_name = os.path.basename(self.context_menu_path)

        if file_name in disabled_files:
            return  # Skip the context menu for disabled files

        if file_name.endswith(".png") or file_name.endswith(".txt"):
            self.context_menu = Menu(self.root, tearoff=0)
            self.context_menu.add_command(label="Edit", command=self.edit_file)
            self.context_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.context_menu = Menu(self.root, tearoff=0)
            self.context_menu.add_command(label="Rename", command=self.rename_folder)
            self.context_menu.add_command(label="Delete", command=self.delete_folder)
            self.context_menu.add_command(label="Properties", command=self.view_properties)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def edit_file(self):
        selected_file = self.context_menu_path

        # Get the full file path
        current_directory = self.path_history[-1]
        full_file_path = os.path.join(current_directory, selected_file)

        # Check if the file is a PNG file
        _, extension = os.path.splitext(full_file_path)
        if extension.lower() == ".png":
            # Create a turtle window
            turtle_screen = turtle.Screen()
            turtle_screen.bgpic(full_file_path)

            # Ask for font size
            font_size = simpledialog.askinteger("Font Size", "Enter the font size (integer):")

            # Ask for font color
            color = colorchooser.askcolor(title="Font Color")
            font_color = color[1]  # Get the hexadecimal font color

            turtle_toplevel = turtle_screen.getcanvas().winfo_toplevel()
            turtle_toplevel.attributes("-topmost", True)

            # Counter for click events
            click_counter = 0
            start_x, start_y = 0, 0
            end_x, end_y = 0, 0

            def on_click(x, y):
                nonlocal click_counter
                nonlocal start_x, start_y, end_y, end_x
                click_counter += 1
                turtle.hideturtle()
                if click_counter == 1:
                    # First click action
                    print("First click:", x, y)
                    turtle.penup()
                    turtle.goto(x, y)  # Position the turtle at the clicked point
                    turtle.dot(10, "black")
                    turtle.write("Start Point is Set", align="center", font=("Arial", 12, "bold"))
                    start_x, start_y = x, y

                elif click_counter == 2:
                    # Second click action
                    print("Second click:", x, y)
                    turtle.penup()
                    turtle.goto(x, y)  # Position the turtle at the clicked point
                    turtle.dot(10, "black")
                    turtle.write("End Point is Set", align="center", font=("Arial", 12, "bold"))
                    end_x, end_y = x, y

                    turtle.onscreenclick(None)

                    # Read lines from names.txt
                    names_file_path = os.path.join(current_directory, "names.txt")
                    with open(names_file_path, "r") as f:
                        lines = f.readlines()

                    # Create the 'certificates' directory if it doesn't exist
                    certificates_dir = os.path.join(current_directory, "certificates")
                    os.makedirs(certificates_dir, exist_ok=True)

                    img = Image.open(os.path.join(current_directory, "sample.png"))
                    draw = ImageDraw.Draw(img)

                    font_path = os.path.join(self.icon_dir, "icons", "arial.ttf")
                    font = ImageFont.truetype(font_path, font_size)

                    # Adjusted coordinates for Pillow reference plane
                    image_width, image_height = img.size
                    start_pillow_x = start_x + image_width // 2
                    start_pillow_y = image_height // 2 - start_y
                    end_pillow_x = end_x + image_width // 2
                    end_pillow_y = image_height // 2 - end_y

                    text_position = ((start_pillow_x + end_pillow_x) // 2, (start_pillow_y + end_pillow_y) // 2)
                    names_list = [line.strip() for line in lines]

                    for name in names_list:
                        certificate_image = img.copy()
                        draw = ImageDraw.Draw(certificate_image)
                        text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:]  # Get width and height from bbox
                        name_x = text_position[0] - text_width // 2
                        name_y = text_position[1] - text_height // 2

                        draw.text((name_x, name_y), name, fill=font_color, font=font)
                        certificate_file_path = os.path.join(certificates_dir, f"{name}.png")
                        certificate_image.save(certificate_file_path)

                        # Print the file path for verification
                        print(f"Saved: {certificate_file_path}")
                        self.refresh()

            turtle.onscreenclick(on_click)  # Register the on_click function
            turtle.done()
 


    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        directories, files = self.get_files_and_directories()

        row, column = 0, 0

        # Display directories
        for directory in directories:
            icon_path = os.path.join(self.icon_dir, "icons","folder_icon.png")
            icon = PhotoImage(file=icon_path)
            label = Label(self.frame, image=icon, text=directory.name, compound="top", padx=10, pady=10)
            label.photo = icon
            label.bind("<Button-1>", lambda event, d=directory: self.open_directory(d.name))
            label.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            column += 1
            if column == 5:
                row += 1
                column = 0

        # Display files
        for file in files:
            icon_path = os.path.join(self.icon_dir,"icons", "file_icon.png")
            icon = PhotoImage(file=icon_path)
            label = Label(self.frame, image=icon, text=file.name, compound="top", padx=10, pady=10)
            label.photo = icon
            label.bind("<Button-1>", lambda event, f=file: self.open_file(f))
            label.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            column += 1
            if column == 5:
                row += 1
                column = 0



if __name__ == "__main__":
    # Check if "MyWorkSpace" directory exists, and create it if necessary
    workspace_dir = "MyWorkSpace"
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)
    # Change the working directory to "MyWorkSpace"
    os.chdir(workspace_dir)
    root = Tk()
    
    file_explorer = FileExplorerGUI(root)

    root.mainloop()