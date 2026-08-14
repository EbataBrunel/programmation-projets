package eajc.group.apv.services;

import eajc.group.apv.dto.ChangePasswordRequest;
import eajc.group.apv.dto.ForgotPasswordRequest;
import eajc.group.apv.dto.ResetPasswordRequest;

public interface PasswordResetService {
    public void forgotPassword(ForgotPasswordRequest request);
    public void resetPassword(ResetPasswordRequest request);
    public void changePassword(String username, ChangePasswordRequest request);
}
