"""
Safety Module
-------------
Provides basic security filtering for code execution.
Blocks dangerous operations and patterns.
"""

import re
from typing import List, Set


class Safety:
    """
    Code safety checker that filters dangerous patterns.

    This is a basic implementation focused on preventing:
    - File system manipulation
    - Network operations
    - System commands
    - Process manipulation
    - Import of dangerous modules
    """

    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r'\beval\b',
        r'\bexec\b',
        r'\bcompile\b',
        r'__import__',
        r'\bopen\(',
        r'\bfile\(',
        r'\bos\.',
        r'\bsys\.',
        r'\bsubprocess\.',
        r'\bshutil\.',
        r'\bpickle\.',
        r'\bsocket\.',
        r'\brequests\.',
        r'\burllib\.',
        r'\bhttplib\.',
        r'\bftplib\.',
        r'\bsmtplib\.',
        r'\btempfile\.',
        r'\bglob\.',
        r'\bpathlib\.',
        r'\.write\(',
        r'\.remove\(',
        r'\.unlink\(',
        r'\.rmdir\(',
        r'\.mkdir\(',
        r'\brm\s',
        r'\bmv\s',
        r'\bcp\s',
        r'\bcurl\s',
        r'\bwget\s',
        r'\bssh\s',
        r'\bscp\s',
        r'\bnc\s',
        r'\bnetcat\s',
    ]

    # Dangerous imports to block
    DANGEROUS_IMPORTS = {
        'os',
        'sys',
        'subprocess',
        'shutil',
        'pathlib',
        'socket',
        'requests',
        'urllib',
        'httplib',
        'ftplib',
        'smtplib',
        'pickle',
        'tempfile',
        'glob',
        'importlib',
    }

    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.DANGEROUS_PATTERNS]

    def is_safe(self, code: str) -> bool:
        """
        Check if code passes safety filters.

        Parameters
        ----------
        code : str
            Code to check

        Returns
        -------
        bool
            True if code is safe, False otherwise
        """
        # Check for dangerous patterns
        for pattern in self.patterns:
            if pattern.search(code):
                return False

        # Check for dangerous imports
        if self._has_dangerous_imports(code):
            return False

        return True

    def _has_dangerous_imports(self, code: str) -> bool:
        """
        Check for dangerous import statements.
        """
        # Match: import os, from os import path, etc.
        import_pattern = r'(?:from\s+(\w+)|import\s+(\w+))'
        matches = re.finditer(import_pattern, code, re.IGNORECASE)

        for match in matches:
            module = match.group(1) or match.group(2)
            if module and module.lower() in self.DANGEROUS_IMPORTS:
                return True

        return False

    def filter_code(self, code: str) -> str:
        """
        Filter and return code if safe, otherwise raise exception.

        Parameters
        ----------
        code : str
            Code to filter

        Returns
        -------
        str
            Original code if safe

        Raises
        ------
        ValueError
            If code contains dangerous patterns
        """
        if not self.is_safe(code):
            raise ValueError("Code contains dangerous patterns and was blocked")
        return code

    def get_violations(self, code: str) -> List[str]:
        """
        Get list of safety violations found in code.

        Parameters
        ----------
        code : str
            Code to check

        Returns
        -------
        List[str]
            List of violation descriptions
        """
        violations = []

        # Check patterns
        for i, pattern in enumerate(self.patterns):
            if pattern.search(code):
                violations.append(f"Dangerous pattern detected: {self.DANGEROUS_PATTERNS[i]}")

        # Check imports
        if self._has_dangerous_imports(code):
            violations.append("Dangerous import detected")

        return violations
