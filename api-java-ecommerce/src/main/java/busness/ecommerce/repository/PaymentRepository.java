package busness.ecommerce.repository;

import busness.ecommerce.entity.Order;
import busness.ecommerce.entity.Payment;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.enums.PaymentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface PaymentRepository extends JpaRepository<Payment, Long> {
    Optional<Payment> findByPaymentIntentId(String intentId);
    List<Payment> findByUser(User user);

    @Query("""
    SELECT COALESCE(SUM(p.amount), 0)
        FROM Payment p
        WHERE p.status = :status
        AND MONTH(p.createdAt) = :month
        AND YEAR(p.createdAt) = :year
    """)
    Double sumByStatusAndMonth(
            @Param("status") PaymentStatus status,
            @Param("month") int month,
            @Param("year") int year
    );

    // 🔥 Revenu du mois (optimisé avec dates)
    @Query("""
        SELECT COALESCE(SUM(p.amount), 0)
        FROM Payment p
        WHERE p.status = :status
        AND p.createdAt BETWEEN :start AND :end
    """)
    Double sumByStatusAndPeriod(
            @Param("status") PaymentStatus status,
            @Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end);

    // Revenu par jour
    @Query("""
        SELECT DATE(p.createdAt), SUM(p.amount)
        FROM Payment p
        WHERE p.status = 'SUCCESS'
        GROUP BY DATE(p.createdAt)
        ORDER BY DATE(p.createdAt)
    """)
    List<Object[]> getDailyRevenue();

    // Revenu total
    @Query("""
        SELECT COALESCE(SUM(p.amount), 0)
        FROM Payment p
        WHERE p.status = 'SUCCESS'
    """)
    Double getTotalRevenue();

    @Query("""
    SELECT COUNT(p)
        FROM Payment p
        WHERE p.status = :status
        AND MONTH(p.createdAt) = :month
        AND YEAR(p.createdAt) = :year
    """)
    Long countPaymentByStatusAndMonth(
            @Param("status") PaymentStatus status,
            @Param("month") int month,
            @Param("year") int year
    );

    @Query("""
    SELECT p
        FROM Payment p
        WHERE p.status = :status
        AND MONTH(p.createdAt) = :month
        AND YEAR(p.createdAt) = :year
    """)
    List<Payment> PaymentsByStatusAndMonth(
            @Param("status") PaymentStatus status,
            @Param("month") int month,
            @Param("year") int year
    );
}
