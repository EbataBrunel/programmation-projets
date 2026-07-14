package busness.ecommerce.services;

import busness.ecommerce.dto.PaymentListDto;
import busness.ecommerce.dto.PaymentRequestDto;
import busness.ecommerce.dto.PaymentResponseDto;
import busness.ecommerce.enums.PaymentStatus;

import java.util.List;
import java.util.Map;

public interface PaymentService {
    PaymentResponseDto createPayment(Long userId, PaymentRequestDto dto);

    // GET
    PaymentResponseDto getPaymentById(Long id);

    // POST
    void confirmPayment(Long paymentId);

    // POST
    void handlePaymentSucceeded(Long paymentId);

    // USER
    List<PaymentListDto> getMyPayments(Long userId);

    // ADMIN
    List<PaymentListDto> getAllPayments();

    // GET
    Double getCurrentMonthRevenue();

    Double getCurrentMonthRevenueByIntervall();

    List<Map<String, Object>> getDailyRevenue();

    Double getTotalRevenue();

    Long getCountCurrentMonthPayment(PaymentStatus status);

    List<PaymentListDto> getPaymentsCurrentMonth(PaymentStatus status);

}
