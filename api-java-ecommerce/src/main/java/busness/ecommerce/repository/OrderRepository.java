package busness.ecommerce.repository;

import busness.ecommerce.entity.Order;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.enums.PaymentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUser(User user);
    List<Order> findByStatusAndCreatedAtBefore(
            OrderStatus status,
            LocalDateTime date
    );
    @Query("""
        SELECT YEAR(o.createdAt), COUNT(o)
        FROM Order o
        GROUP BY YEAR(o.createdAt)
        ORDER BY YEAR(o.createdAt)
    """)
    List<Object[]> countOrdersByYear();

    @Query("""
        SELECT MONTH(o.createdAt), COUNT(o)
        FROM Order o
        WHERE YEAR(o.createdAt) = :year
        GROUP BY MONTH(o.createdAt)
        ORDER BY MONTH(o.createdAt)
    """)
    List<Object[]> countOrdersByMonth(@Param("year") int year);


    @Query("""
    SELECT COUNT(o)
        FROM Order o
        WHERE o.status = :status
        AND MONTH(o.createdAt) = :month
        AND YEAR(o.createdAt) = :year
    """)
    Long countOrderByStatusAndMonth(
            @Param("status") OrderStatus status,
            @Param("month") int month,
            @Param("year") int year
    );

    @Query("""
    SELECT o
        FROM Order o
        WHERE o.status = :status
        AND MONTH(o.createdAt) = :month
        AND YEAR(o.createdAt) = :year
    """)
    List<Order> ordersByStatusAndMonth(
            @Param("status") OrderStatus status,
            @Param("month") int month,
            @Param("year") int year
    );

}
