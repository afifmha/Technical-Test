# Main Design Decisions
Main design decision is based on SOLID Principles especially on Single Responsibility Principle and Dependency Inversion Principle. Where iam split the structure into Router for request handling, RagServices for Business logic and VectorStore for Data Access, so each component has only one spesific reason to change.
# Trade-off Considered
The Trade-off i took is complex system design for achieving Open Close Principle that made to create a lot boilerplate and files. This make adding or removing new feature didn't modify running business logic and bug can be minimized.
# Improvements to Maintainability
This make code structure easier to maintain, because both databases have same rule from dependencies.
