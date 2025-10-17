"""
FABRIK (Forward And Backward Reaching Inverse Kinematics) Solver
Implementation of the FABRIK algorithm for 2D inverse kinematics.
"""
import numpy as np
import math


def unitVector(vector):
    """Returns the unit vector of a given input vector."""
    return vector / np.linalg.norm(vector)


class Segment2D:
    """Represents a single segment in the kinematic chain."""
    
    def __init__(self, referenceX, referenceY, length, angle):
        """
        Initialize a segment.
        
        Args:
            referenceX: X coordinate of the reference point
            referenceY: Y coordinate of the reference point
            length: Length of the segment
            angle: Initial angle in degrees
        """
        self.angle = angle
        self.length = length
        
        deltaX = math.cos(math.radians(angle)) * length
        deltaY = math.sin(math.radians(angle)) * length
        
        self.point = np.array([referenceX + deltaX, referenceY + deltaY])


class FabrikSolver2D:
    """FABRIK Inverse Kinematics solver for 2D space."""
    
    def __init__(self, baseX=0, baseY=0, marginOfError=0.01):
        """
        Initialize the FABRIK solver.
        
        Args:
            baseX: X coordinate of the fixed base point
            baseY: Y coordinate of the fixed base point
            marginOfError: Distance threshold for convergence
        """
        self.basePoint = np.array([baseX, baseY])
        self.segments = []
        self.armLength = 0
        self.marginOfError = marginOfError
    
    def addSegment(self, length, angle):
        """
        Add a new segment to the kinematic chain.
        
        Args:
            length: Length of the segment
            angle: Initial angle in degrees
        """
        if len(self.segments) > 0:
            segment = Segment2D(self.segments[-1].point[0], self.segments[-1].point[1], 
                               length, angle + self.segments[-1].angle)
        else:
            segment = Segment2D(self.basePoint[0], self.basePoint[1], length, angle)
        
        self.armLength += segment.length
        self.segments.append(segment)
    
    def isReachable(self, targetX, targetY):
        """
        Check if target is within reachable distance.
        
        Args:
            targetX: Target X coordinate
            targetY: Target Y coordinate
            
        Returns:
            True if target is reachable, False otherwise
        """
        distance = np.linalg.norm(self.basePoint - np.array([targetX, targetY]))
        return distance < self.armLength
    
    def inMarginOfError(self, targetX, targetY):
        """
        Check if end effector is within margin of error of target.
        
        Args:
            targetX: Target X coordinate
            targetY: Target Y coordinate
            
        Returns:
            True if within margin, False otherwise
        """
        distance = np.linalg.norm(self.segments[-1].point - np.array([targetX, targetY]))
        return distance < self.marginOfError
    
    def iterate(self, targetX, targetY):
        """
        Perform one iteration of the FABRIK algorithm.
        
        Args:
            targetX: Target X coordinate
            targetY: Target Y coordinate
        """
        target = np.array([targetX, targetY])
        
        # Backward reaching (from end effector to base)
        for i in range(len(self.segments) - 1, 0, -1):
            if i == len(self.segments) - 1:
                self.segments[i-1].point = (unitVector(self.segments[i-1].point - target) * 
                                           self.segments[i].length) + target
            else:
                self.segments[i-1].point = (unitVector(self.segments[i-1].point - self.segments[i].point) * 
                                           self.segments[i].length) + self.segments[i].point
        
        # Forward reaching (from base to end effector)
        for i in range(len(self.segments)):
            if i == 0:
                self.segments[i].point = (unitVector(self.segments[i].point - self.basePoint) * 
                                         self.segments[i].length) + self.basePoint
            elif i == len(self.segments) - 1:
                self.segments[i].point = (unitVector(self.segments[i-1].point - target) * 
                                         self.segments[i].length * -1) + self.segments[i-1].point
            else:
                self.segments[i].point = (unitVector(self.segments[i].point - self.segments[i-1].point) * 
                                         self.segments[i].length) + self.segments[i-1].point
    
    def compute(self, targetX, targetY):
        """
        Solve inverse kinematics to reach the target position.
        
        Args:
            targetX: Target X coordinate
            targetY: Target Y coordinate
            
        Returns:
            True if target was reached, False if unreachable
        """
        if not self.isReachable(targetX, targetY):
            return False
            
        while not self.inMarginOfError(targetX, targetY):
            self.iterate(targetX, targetY)
        
        return True
    
    def get_joint_positions(self):
        """
        Get all joint positions including the base point.
        
        Returns:
            List of [x, y] coordinate pairs
        """
        positions = [self.basePoint.tolist()]
        for segment in self.segments:
            positions.append(segment.point.tolist())
        return positions
