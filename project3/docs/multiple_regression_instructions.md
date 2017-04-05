# Steps for Multiple Regression
Generally, follow the guidelines: [Multiple Linear Regression][guidelines] (pages 16-18).

To find the coefficients for a simple multiple regression equation predicting the income of a household in the given region based on knowledge of the age of head of household, number of occupants,
and rent/own status.

## STEPS:
1. Create an `array` of `Income` values (Y)
2. Create a 2D `array` (X) with `4` columns:
    1. Column `1` = `1s` in all rows
    2. Column `2` = the age of head of households
    3. Column `3` = The number of household occupants
    4. Column `4` = `1` if home is owned, `0` if rented
3. Find the matrix of coefficients (Using the [Java Matrix Class][java_matrix])
```java
b = X^(t*X) ^ (-1 * X^(t*Y));
```
4. Return the coefficients for each region.

<!-- references -->
[guidelines]: https://onlinecourses.science.psu.edu/stat501/sites/onlinecourses.science.psu.edu.stat501/files/pt2_multiple_linear_regression.pdf "Multiple Linear Regression"
[java_matrix]: http://math.nist.gov/javanumerics/jama/doc/
