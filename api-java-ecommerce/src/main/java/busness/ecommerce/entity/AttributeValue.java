package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class AttributeValue {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String value; // M, L, Rouge, Coton

    @ManyToOne
    @JoinColumn(name = "attribute_id")
    private Attribute attribute;
}

