package busness.ecommerce.entity;

import busness.ecommerce.enums.Gender;
import jakarta.persistence.*;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Entity
@Data
public class ProductVariant {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String sku;
    private Double price;
    private Integer stock;
    // ===== Type =====
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Gender gender; // HOMME / FEMME / ENFANT

    @ManyToOne
    private Product product;

    @OneToMany(mappedBy = "variant", cascade = CascadeType.ALL)
    private List<ProductAttribute> attributes;
}

