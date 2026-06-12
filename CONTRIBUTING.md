# Contributing to NEXT-FORGE-sim2real

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

All contributors agree to follow our Code of Conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Report issues appropriately

## How to Contribute

### 1. Reporting Bugs

Before creating bug reports, check the issue list as you might find out that you don't need to create one.

**When creating a bug report, include:**
- Clear description of the issue
- Steps to reproduce the problem
- Specific examples to demonstrate the steps
- Description of observed behavior
- Description of expected behavior
- Possible suggestions for the fix

### 2. Suggesting Enhancements

**When creating enhancement suggestions, include:**
- Clear description of the enhancement
- Step-by-step description of the suggested enhancement
- Specific examples to demonstrate the steps
- Possible implementation approach

### 3. Development Workflow

#### Step 1: Fork the Repository
```bash
git clone https://github.com/YOUR-USERNAME/NEXT-FORGE-sim2real.git
cd NEXT-FORGE-sim2real
git remote add upstream https://github.com/ORIGINAL-REPO/NEXT-FORGE-sim2real.git
```

#### Step 2: Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### Step 3: Make Your Changes
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-documented

#### Step 4: Test Your Changes

**For Docker:**
```bash
./docker_manager.sh build
./docker_manager.sh start
./docker_manager.sh test
```

**For Native:**
```bash
cd ~/ros_projects/ros2_ws
./scripts/initial_build.bash
source install/setup.bash
colcon test
```

#### Step 5: Commit Your Changes
```bash
git add .
git commit -m "Add meaningful commit message"
# Use imperative mood ("Add feature" not "Added feature")
# Reference issues/PRs: "Fixes #123"
```

#### Step 6: Push to Your Fork
```bash
git push origin feature/your-feature-name
```

#### Step 7: Create a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR title and description
5. Submit the PR

### 4. Pull Request Guidelines

**PR Title:**
- Use clear, descriptive titles
- Reference related issues: `[Fix #123] Add probe detection`

**PR Description:**
- Describe what changes were made
- Explain why these changes are needed
- Reference any related issues or PRs
- Include screenshots/videos if relevant

**PR Checklist:**
- [ ] Code follows project style guide
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or justified)
- [ ] Commits are atomic and well-described

## Coding Guidelines

### Python Code Style

Follow PEP 8 with the following additions:

```python
# Good - clear and descriptive
def detect_probe_position(transform_msg: TransformStamped) -> List[float]:
    """Extract probe position from transform message.
    
    Args:
        transform_msg: ROS2 TransformStamped message
        
    Returns:
        List of [x, y, z] coordinates
    """
    x = transform_msg.transform.translation.x
    y = transform_msg.transform.translation.y
    z = transform_msg.transform.translation.z
    return [x, y, z]

# Bad - unclear
def get_pos(t):
    return [t.transform.translation.x, t.transform.translation.y, t.transform.translation.z]
```

**Guidelines:**
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused
- Use descriptive variable names
- Maximum line length: 100 characters

### ROS2/XML Guidelines

```xml
<!-- Good - clear hierarchy and naming -->
<body name="probe_link" pos="0 0 0.05">
    <geom name="probe_collision" type="cylinder" size="0.01 0.05"/>
    <geom name="probe_visual" type="mesh" mesh="probe"/>
</body>

<!-- Bad - unclear structure -->
<body name="p">
    <geom type="cylinder" size="0.01 0.05"/>
</body>
```

### Commit Messages

```
Add probe detection algorithm in sim adapter

- Implement distance-based detection
- Add threshold configuration
- Include unit tests

Fixes #42
```

**Format:**
- First line: 50 characters or less, clear summary
- Blank line
- Detailed explanation (wrap at 72 characters)
- Reference issues with "Fixes #123"

## File Structure

When adding new features:

```
src/new_package/
├── new_package/
│   ├── __init__.py
│   ├── module.py           # Implementation
│   └── [other modules]
├── launch/
│   └── example_launch.py
├── config/
│   └── config.json
├── docs/
│   └── MODULE_GUIDE.md
├── examples/
│   └── example_usage.py
├── test/
│   ├── test_module.py
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.py
├── setup.cfg
└── README.md
```

## Documentation

### Update These When Contributing:

1. **Code Comments** - Explain complex logic
2. **Docstrings** - Document all public APIs
3. **README.md** - Update if adding major features
4. **CHANGELOG** - Document your changes
5. **Examples** - Add usage examples for new features

### Documentation Standards:

```python
def calculate_distance(point1: Tuple[float, float, float],
                      point2: Tuple[float, float, float]) -> float:
    """Calculate Euclidean distance between two 3D points.
    
    This function computes the distance in 3D space using the
    standard Euclidean distance formula.
    
    Args:
        point1: First point as (x, y, z) tuple
        point2: Second point as (x, y, z) tuple
        
    Returns:
        Distance as float value in meters
        
    Raises:
        TypeError: If points are not tuples of length 3
        
    Examples:
        >>> dist = calculate_distance((0, 0, 0), (1, 1, 1))
        >>> abs(dist - 1.732) < 0.01
        True
    """
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]
    z_diff = point1[2] - point2[2]
    return (x_diff**2 + y_diff**2 + z_diff**2)**0.5
```

## Testing

### Unit Tests

```python
# test_probe_detection.py
import pytest
from sim_hardware_adapter import is_probe_in_detection_zone

class TestProbeDetection:
    def test_probe_detected_above_threshold(self):
        """Probe should be detected when z > -0.01"""
        position = [0.0, 0.0, 0.0]  # Above board
        assert is_probe_in_detection_zone(position) == True
    
    def test_probe_not_detected_below_threshold(self):
        """Probe should not be detected when z < -0.01"""
        position = [0.0, 0.0, -0.02]
        assert is_probe_in_detection_zone(position) == False
    
    def test_probe_boundary_condition(self):
        """Test boundary at z = -0.01"""
        position = [0.0, 0.0, -0.01]
        assert is_probe_in_detection_zone(position) == True
```

### Integration Tests

Test between components:
```bash
# Test bridge with simulator
./docker_manager.sh sim &
# In another terminal
docker exec -it ros2_taskboard pytest test/integration/
```

### Run Tests

```bash
# All tests
colcon test

# Specific package
colcon test --packages-select board_hardware_bridge

# With output
colcon test --packages-select board_hardware_bridge --ctest-args --verbose
```

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Example: `v1.2.3`

## Release Process

When releasing a new version:

1. Update version in package.xml files
2. Update CHANGELOG.md
3. Create tagged commit: `git tag v1.2.3`
4. Push tag: `git push origin v1.2.3`
5. Create GitHub release with notes

## Getting Help

- Check existing issues and documentation
- Ask in GitHub Discussions
- Contact maintainers for detailed questions

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

## Additional Notes

- We use GitHub Issues for tracking
- Pull Requests are the main way to contribute
- All code should be tested before submission
- Documentation is as important as code

Thank you for contributing to NEXT-FORGE-sim2real! 🚀
