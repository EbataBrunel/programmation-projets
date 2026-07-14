package busness.ecommerce.entity;

import busness.ecommerce.enums.OrderStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "orders") // mot réservé SQL
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // utilisateur
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    // date
    private LocalDateTime createdAt;

    // statut
    @Enumerated(EnumType.STRING)
    @Column(length = 30)
    private OrderStatus status;

    // total
    private Double total;

    // produits commandés
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItem> items = new ArrayList<>();
}

