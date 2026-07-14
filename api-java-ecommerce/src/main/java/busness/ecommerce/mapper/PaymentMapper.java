package busness.ecommerce.mapper;

import busness.ecommerce.dto.PaymentListDto;
import busness.ecommerce.dto.PaymentResponseDto;
import busness.ecommerce.entity.Payment;
import org.springframework.stereotype.Component;

@Component
public class PaymentMapper {

    public PaymentResponseDto toDto(Payment payment){
        return PaymentResponseDto.builder()
                .paymentId(payment.getId())
                .paymentIntentId(payment.getPaymentIntentId())
                .status(payment.getStatus().name())
                .amount(payment.getAmount())
                .mode(payment.getMode().name())
                .build();
    }
    public PaymentListDto toListDto(Payment payment) {
        return PaymentListDto.builder()
                .id(payment.getId())
                .amount(payment.getAmount())
                .status(payment.getStatus().name())
                .mode(payment.getMode())
                .createdAt(payment.getCreatedAt())
                .orderId(payment.getOrder().getId())
                .build();
    }
}
