package busness.ecommerce.controller;

import busness.ecommerce.dto.PaymentListDto;
import busness.ecommerce.dto.PaymentRequestDto;
import busness.ecommerce.dto.PaymentResponseDto;
import busness.ecommerce.enums.PaymentStatus;
import busness.ecommerce.services.CustomUserDetails;
import busness.ecommerce.services.PaymentService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping(value="/api/v1/payments")
@RequiredArgsConstructor
public class PaymentRestController {
    private final PaymentService paymentService;

    @PostMapping
    public ResponseEntity<PaymentResponseDto> createPayment(
            @RequestBody PaymentRequestDto dto,
            Authentication authentication
    ) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("User not authenticated");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(
                paymentService.createPayment(user.getUser().getId(), dto)
        );
    }

    // USER
    @GetMapping("/user/{userId}")
    public List<PaymentListDto> myPayments(@PathVariable Long userId) {
        return paymentService.getMyPayments(userId);
    }

    // ADMIN
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public List<PaymentListDto> allPayments() {
        return paymentService.getAllPayments();
    }

    @GetMapping("/revenue/month")
    public ResponseEntity<Double> getCurrentMonthRevenue() {
        return ResponseEntity.ok(paymentService.getCurrentMonthRevenue());
    }

    // Revenu du mois
    @GetMapping("/revenue/month/interval")
    public ResponseEntity<Double> getCurrentMonthRevenueByIntervall() {
        return ResponseEntity.ok(paymentService.getCurrentMonthRevenueByIntervall());
    }

    // Revenu journalier (graph)
    @GetMapping("/revenue/daily")
    public ResponseEntity<List<Map<String, Object>>> getDailyRevenue() {
        return ResponseEntity.ok(paymentService.getDailyRevenue());
    }

    // 💰 Revenu total
    @GetMapping("/revenue/total")
    public ResponseEntity<Double> getTotalRevenue() {
        return ResponseEntity.ok(paymentService.getTotalRevenue());
    }

    @PostMapping("/confirm/{paymentId}")
    public ResponseEntity<?> confirmPayment(@PathVariable Long paymentId){
        System.out.println("ID "+paymentId);
        paymentService.confirmPayment(paymentId);

        return ResponseEntity.ok("Payment confirmed");
    }

    @GetMapping("/count/month/{status}")
    public ResponseEntity<Long> getCountPaymentsCurrentMonth(
            @PathVariable PaymentStatus status
    ) {
        return ResponseEntity.ok(paymentService.getCountCurrentMonthPayment(status));
    }

    @GetMapping("/month/{status}")
    public ResponseEntity<List<PaymentListDto>> getPaymentsCurrentMonth(
            @PathVariable PaymentStatus status
    ) {
        return ResponseEntity.ok(paymentService.getPaymentsCurrentMonth(status));
    }
}
