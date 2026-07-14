package busness.ecommerce.services;

import busness.ecommerce.dto.ForgotPasswordRequestDto;
import busness.ecommerce.dto.ResetPasswordRequestDto;

public interface AuthService {
    void forgotPassword(ForgotPasswordRequestDto request);
    void resetPassword(ResetPasswordRequestDto request);
}
