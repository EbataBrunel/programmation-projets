package eajc.group.apv.entity;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "events")
public class Event {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(unique = true, nullable = false, length = 200)
    private String name;

    @Column(nullable = false)
    private BigDecimal mount;

    @Column(nullable = true)
    private BigDecimal amountTotal;

    @Column(nullable = false)
    private LocalDate eventDate;

    @Column(nullable = false)
    private Boolean closure_status;

    @Column(nullable = true, columnDefinition = "TEXT")
    private String comment;

    @ManyToOne
    @JoinColumn(name = "event_type_id")
    private EventType eventType;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    @OneToMany(mappedBy = "event", cascade = CascadeType.ALL)
    private List<Contribution> contributions = new ArrayList<>();

    public Event(){}

    public Event(Long id, UUID publicId, String name, BigDecimal mount, BigDecimal amountTotal, LocalDate eventDate, Boolean closure_status, String comment, EventType eventType, User user, List<Contribution> contributions) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.mount = mount;
        this.amountTotal = amountTotal;
        this.eventDate = eventDate;
        this.closure_status = closure_status;
        this.comment = comment;
        this.eventType = eventType;
        this.user = user;
        this.contributions = contributions;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getMount() {
        return mount;
    }

    public void setMount(BigDecimal mount) {
        this.mount = mount;
    }

    public BigDecimal getAmountTotal() {
        return amountTotal;
    }

    public void setAmountTotal(BigDecimal amountTotal) {
        this.amountTotal = amountTotal;
    }

    public LocalDate getEventDate() {
        return eventDate;
    }

    public void setEventDate(LocalDate eventDate) {
        this.eventDate = eventDate;
    }

    public Boolean getClosure_status() {
        return closure_status;
    }

    public void setClosure_status(Boolean closure_status) {
        this.closure_status = closure_status;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public EventType getEventType() {
        return eventType;
    }

    public void setEventType(EventType eventType) {
        this.eventType = eventType;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public List<Contribution> getContributions() {
        return contributions;
    }

    public void setContributions(List<Contribution> contributions) {
        this.contributions = contributions;
    }

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }
    }
}
