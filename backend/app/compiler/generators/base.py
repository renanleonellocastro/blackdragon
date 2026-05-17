"""Abstract base generator interface."""
from abc import ABC, abstractmethod

from app.compiler.ir import IR


class BaseGenerator(ABC):
    """Base class for code generators."""

    @abstractmethod
    def generate(self, ir: IR, context: dict) -> str:
        """Generate target code from the IR.

        Args:
            ir: The optimized intermediate representation.
            context: Additional context (board info, credentials, etc.)

        Returns:
            Generated code as a string.
        """
        ...

    @abstractmethod
    def file_extension(self) -> str:
        """Return the file extension for generated output."""
        ...
