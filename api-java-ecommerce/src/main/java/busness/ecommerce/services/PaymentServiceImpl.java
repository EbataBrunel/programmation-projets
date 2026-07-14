package busness.ecommerce.services;

import busness.ecommerce.dto.PaymentListDto;
import busness.ecommerce.dto.PaymentRequestDto;
import busness.ecommerce.dto.PaymentResponseDto;
import busness.ecommerce.entity.Cart;
import busness.ecommerce.entity.Order;
import busness.ecommerce.entity.Payment;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.ModePayment;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.enums.PaymentStatus;
import busness.ecommerce.mapper.PaymentMapper;
import busness.ecommerce.repository.CartRepository;
import busness.ecommerce.repository.OrderRepository;
import busness.ecommerce.repository.PaymentRepository;
import busness.ecommerce.repository.UserRepository;
//import com.stripe.model.PaymentIntent;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Transactional
public class PaymentServiceImpl implements PaymentService{

    private  final UserRepository userRepository;
    private final OrderRepository orderRepository;
    private final PaymentRepository paymentRepository;
    private final StripeService stripeService;
    private final PaymentMapper paymentMapper;
    private final CartRepository cartRepository;
    //private FrontendProperties frontendProperties;

    /**
     * 🔥 1. Création du paiement + session Stripe
     */
    @Override
    public PaymentResponseDto createPayment(Long userId, PaymentRequestDto dto) {

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Order order = orderRepository.findById(dto.getOrderId())
                .orElseThrow(() -> new RuntimeException("Order not found"));

        if (!order.getUser().getId().equals(userId)) {
            throw new RuntimeException("Not your order");
        }

        try {

            Payment payment = Payment.builder()
                    .order(order)
                    .amount(order.getTotal())
                    .status(PaymentStatus.PENDING)
                    .mode(dto.getMode())
                    .user(user)
                    .createdAt(LocalDateTime.now())
                    .build();

            paymentRepository.save(payment);

            String redirectUrl = "";
            if ("CARD".equals(dto.getMode().toString())) {
                // Préparer metadata pour Stripe
                Map<String, String> metadata = new HashMap<>();
                metadata.put("paymentId", payment.getId().toString());

                // Créer session Stripe
                redirectUrl = stripeService.createCheckoutSession(order.getTotal(), metadata);
            }

            // Retour frontend

            return PaymentResponseDto.builder()
                    .paymentId(payment.getId())
                    //.paymentIntentId(payment.getPaymentIntentId())
                    //.clientSecret(intent.getClientSecret())
                    .mode(payment.getMode().name())
                    .status(payment.getStatus().name())
                    .amount(payment.getAmount())
                    .redirectUrl(redirectUrl)
                    .build();

        } catch (Exception e) {
            throw new RuntimeException("Payment error");
        }
    }

    @Override
    public PaymentResponseDto getPaymentById(Long id) {
        Payment payment = paymentRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Payment not found"));
        return paymentMapper.toDto(payment);
    }

    /**
     * Méthode appelée depuis le webhook Stripe quand le paiement est réussi
     */
    @Override
    public void handlePaymentSucceeded(Long paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new RuntimeException("Payment not found"));

        // Mettre à jour le paiement
        payment.setStatus(PaymentStatus.SUCCESS);

        // Mettre à jour la commande
        Order order = payment.getOrder();
        order.setStatus(OrderStatus.PAID);

        // Vider le panier de l'utilisateur
        User user = payment.getUser();
        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found"));

        cart.getItems().clear();
        cart.setQtyTotal(0);
        cart.setTotal(0.0);

        // 🔥 Sauvegarde finale
        cartRepository.save(cart);
        paymentRepository.save(payment);
    }

    @Override
    public void confirmPayment(Long paymentId) {

        Payment payment = paymentRepository
                .findById(paymentId)
                .orElseThrow();

        payment.setStatus(PaymentStatus.SUCCESS);

        Order order = payment.getOrder();
        order.setStatus(OrderStatus.PAID);

        User user = payment.getUser();

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found"));

        cart.getItems().clear();
        cart.setQtyTotal(0);
        cart.setTotal(0.0);

        cartRepository.save(cart);
        paymentRepository.save(payment);
        orderRepository.save(order);
    }

    @Override
    public List<PaymentListDto> getMyPayments(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        return paymentRepository.findByUser(user)
                .stream()
                .map(paymentMapper::toListDto)
                .toList();
    }

    @Override
    public List<PaymentListDto> getAllPayments() {
        return paymentRepository.findAll()
                .stream()
                .map(paymentMapper::toListDto)
                .toList();
    }

    @Override
    public Double getCurrentMonthRevenue() {
        LocalDateTime now = LocalDateTime.now();

        int month = now.getMonthValue();
        int year = now.getYear();

        return paymentRepository.sumByStatusAndMonth(
                PaymentStatus.SUCCESS,
                month,
                year
        );
    }

    @Override
    public Double getCurrentMonthRevenueByIntervall() {
        LocalDateTime start = LocalDate.now()
                .withDayOfMonth(1)
                .atStartOfDay();

        LocalDateTime end = start.plusMonths(1);

        return paymentRepository.sumByStatusAndPeriod(
                PaymentStatus.SUCCESS,
                start,
                end
        );

    }

    @Override
    public List<Map<String, Object>> getDailyRevenue() {
        return paymentRepository.getDailyRevenue()
                .stream()
                .map(obj -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("date", obj[0]);
                    map.put("total", obj[1]);
                    return map;
                })
                .toList();
    }

    @Override
    public Double getTotalRevenue() {
        return paymentRepository.getTotalRevenue();
    }

    @Override
    public Long getCountCurrentMonthPayment(PaymentStatus status) {
        LocalDateTime now = LocalDateTime.now();

        int month = now.getMonthValue();
        int year = now.getYear();
        return paymentRepository.countPaymentByStatusAndMonth(
                status,
                month,
                year
        );
    }

    @Override
    public List<PaymentListDto> getPaymentsCurrentMonth(PaymentStatus status) {
        LocalDateTime now = LocalDateTime.now();

        int month = now.getMonthValue();
        int year = now.getYear();
        return paymentRepository.PaymentsByStatusAndMonth(status, month, year)
                .stream()
                .map(paymentMapper::toListDto)
                .toList();
    }
}
