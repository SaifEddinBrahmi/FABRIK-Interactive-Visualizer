# 🤖 FABRIK Interactive Visualizer

An interactive real-time visualization of the **FABRIK (Forward And Backward Reaching Inverse Kinematics)** algorithm. Click anywhere on the screen and watch the robotic arm smoothly move to reach that point!

## 🎬 Demo

![FABRIK Demo](demo.gif)

*Click anywhere to move the arm - the end effector reaches the target precisely!*

## 🎯 Features

- **Interactive Control**: Click anywhere to set a new target position
- **Real-time Visualization**: Watch the arm solve inverse kinematics instantly
- **Visual Feedback**: 
  - Green target indicator for reachable positions
  - Red indicator for unreachable positions
  - Live coordinate display
- **Professional UI**: Clean, modern interface with grid and legend
- **Smooth Performance**: 60 FPS rendering

## 🧠 What is FABRIK?

FABRIK (Forward And Backward Reaching Inverse Kinematics) is an efficient algorithm for solving inverse kinematics problems. It works by:

1. **Backward Pass**: Starting from the end effector, reach toward the target
2. **Forward Pass**: Starting from the base, restore the chain's constraints
3. **Iterate**: Repeat until the end effector reaches the target

This approach is simpler and faster than traditional Jacobian-based methods!

## 🚀 Installation

### Requirements
- Python 3.10 or higher
- Pygame
- NumPy

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/FABRIK-Interactive-Visualizer.git
cd FABRIK-Interactive-Visualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:
```bash
python main.py
```

### Controls
- **Left Click**: Set a new target position for the arm to reach
- **Close Window**: Exit the application

### Visual Elements
- 🟡 **Yellow Circle**: Base point (fixed anchor)
- 🔴 **Red Circles**: Joint positions
- 🟢 **Green Circle**: End effector (tip of the arm)
- ✚ **Crosshair**: Target position
  - Green = Reachable
  - Red = Out of reach

## 📁 Project Structure

```
FABRIK-Interactive-Visualizer/
├── main.py              # Entry point
├── solver.py            # FABRIK algorithm implementation
├── visualizer.py        # Pygame interactive window
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🔧 Technical Details

### FABRIK Algorithm
The solver uses the FABRIK algorithm with:
- **Margin of Error**: 2 pixels (configurable)
- **Max Iterations**: 100 per solve
- **Convergence**: Iterates until end effector is within margin of target

### Arm Configuration
- **Segments**: 3 segments (150px, 120px, 100px)
- **Total Reach**: 370 pixels from base
- **Degrees of Freedom**: 3 (one per segment)

### Performance
- **Rendering**: 60 FPS
- **Solve Time**: < 1ms for typical cases
- **Resolution**: 1000x700 pixels (configurable)

## 🎓 Use Cases

This project demonstrates concepts useful for:
- **Robotics**: Robot arm control and planning
- **Animation**: Character IK for games and movies
- **Computer Graphics**: Procedural animation systems
- **Education**: Learning inverse kinematics algorithms

## 🛠️ Customization

### Change Arm Configuration
Edit `visualizer.py` in the `__init__` method:
```python
self.solver.add_segment(150, 0)  # Length, initial angle
self.solver.add_segment(120, 0)
self.solver.add_segment(100, 0)
```

### Adjust Window Size
Pass parameters when creating the visualizer:
```python
app = FabrikVisualizer(width=1200, height=800)
```

### Modify Margin of Error
In `visualizer.py`:
```python
self.solver = FabrikSolver2D(center_x, center_y, margin_of_error=5)
```

## 📚 References

- **Original Paper**: [FABRIK: A fast, iterative solver for the Inverse Kinematics problem](http://www.andreasaristidou.com/publications/papers/FABRIK.pdf) by Andreas Aristidou and Joan Lasenby (2011)
- **Algorithm**: Forward And Backward Reaching Inverse Kinematics

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Saif Eddin Brahmi**
- GitHub: [@SaifEddinBrahmi](https://github.com/SaifEddinBrahmi)
- LinkedIn: [Saif Eddin Brahmi](https://www.linkedin.com/in/saif-eddin-brahmi/)

## 🌟 Acknowledgments

- Andreas Aristidou and Joan Lasenby for the FABRIK algorithm
- Pygame community for the excellent game development library

---

**Star ⭐ this repo if you find it useful!**
