"""
FABRIK Interactive Visualizer
Main entry point for the application
"""
from visualizer import FabrikVisualizer


def main():
    """Launch the interactive FABRIK visualizer."""
    print("=" * 60)
    print("FABRIK Interactive Visualizer")
    print("=" * 60)
    print("\nStarting application...")
    print("\nInstructions:")
    print("  • Click anywhere in the window to set a target")
    print("  • The robotic arm will move to reach that point")
    print("  • Green target = reachable")
    print("  • Red target = out of reach")
    print("  • Close window to exit")
    print("\n" + "=" * 60 + "\n")
    
    # Create and run visualizer
    app = FabrikVisualizer(width=1000, height=700)
    app.run()


if __name__ == "__main__":
    main()
