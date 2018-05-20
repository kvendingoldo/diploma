def calculate_element(self, element, variables):
   print('I am alive')

   x1, x2 = symbols('x_1 x_2')
   f_eq1 = 0
   f_eq2 = 0
   f_eq3 = 0
   for k in range(0, self.M):
       n_k = element.get_basic_function_by_number(k)
       weight_functions = 0
       print('I am still alive. [element=%s, k=%d]' % (str(element), k))
       for l in range(0, self.M):
           w_l = element.get_basic_function_by_number(l)
           weight_functions += w_l
           f_eq1 += \
               + element.integrate(w_l * diff(
                   -P_a * H0 - P_a * variables[2 * self.M + k] * n_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 *
                   variables[2 * self.M + k] * n_k - g * rho / 2 * variables[2 * self.M + k] ** 2 * n_k ** 2, x1)) \
               + element.integrate(P_a * w_l * diff(H0 + variables[2 * self.M + k] * n_k, x1)) \
               + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * w_l) \
               - element.integrate(
                   (gc2 * w_l * variables[k] / (rho * H0 ** 2) * variables[2 * self.M + k] ** 2 * n_k) * sqrt(
                       variables[k] ** 2 * n_k ** 2 + variables[self.M + k] ** 2 * n_k ** 2))

           f_eq2 += \
               + element.integrate(w_l * diff(
                   -P_a * H0 - P_a * variables[2 * self.M + k] * n_k - ((g * rho / 2) * H0 ** 2) - g * rho * H0 *
                   variables[2 * self.M + k] * n_k - g * rho / 2 * variables[2 * self.M + k] ** 2 * n_k ** 2, x2)) \
               + element.integrate(P_a * w_l * diff(H0 + variables[2 * self.M + k] * n_k, x2)) \
               + element.integrate(sqrt(2) / 2 * W ** 2 * gamma * rho_a * w_l) \
               - element.integrate(
                   (gc2 * w_l * variables[self.M + k] / (rho * H0 ** 2) * variables[
                       2 * self.M + k] ** 2 * n_k) * sqrt(
                       variables[k] ** 2 * n_k ** 2 + variables[self.M + k] ** 2 * n_k ** 2))

           f_eq3 += \
               - element.integrate(w_l * diff(n_k, x1)) * variables[k] \
               - element.integrate(w_l * diff(n_k, x2)) * variables[self.M + k]

       coefficient_of_d_eq1 = element.integrate(weight_functions * n_k)
       coefficient_of_d_eq2 = element.integrate(weight_functions * n_k)
       coefficient_of_d_eq3 = element.integrate(rho * weight_functions * n_k)

       if coefficient_of_d_eq1 != 0:
           if self.on_boundary(element, k):
               self.sys_fun[k] = 0
           else:
               self.sys_fun[k] = Float((f_eq1.evalf() / coefficient_of_d_eq1))

       if coefficient_of_d_eq2 != 0:
           if self.on_boundary(element, k):
               self.sys_fun[self.M + k] = 0
           else:
               self.sys_fun[self.M + k] = Float((f_eq2.evalf() / coefficient_of_d_eq2))

       if coefficient_of_d_eq3 != 0:
           if self.on_boundary(element, k):
               self.sys_fun[2 * self.M + k] = 0
           else:
               self.sys_fun[2 * self.M + k] = Float((f_eq3.evalf() / coefficient_of_d_eq3))

   print('I am dead')
