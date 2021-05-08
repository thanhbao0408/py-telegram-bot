let arrayOfProjects = ["[Planner] - [Angular] - Add/Edit Basket Modal 123"];

// For Performance. Reading the array in sequence instead of parallel
for (const project of arrayOfProjects) {
    await $.post(
        "http://105devpmasql:9991/project/submitportal/", {
    __RequestVerificationToken:
      "7p540mfW8RBvkr5a2BXmCZD9WHq3FcXHa5G_XEZbV6Tt8swczR8m4CXVlQHHYK4EsTmu2TQff6-4xqZiQO1OYrfzu7PAX4gRcFX1TS3sVID9KOtLDNqffnSqvoRzlY7k0",
    IsAutoGenerateProjectNo: true,
    IsShowListPrefix: true,
    PrefixName: "PMA",
    ProjectName: project,
    ScopeId: 12,
    ServiceTypeId: "b4d8200c-5566-498b-8d03-a8a70097cd67",
    BranchId: "3d4e34b9-6ace-49dc-a96e-a7eb0071e9f5",
    PriorityId: "ff688692-5ded-4ca9-83cc-779ebef210b9",
    IsRequestor: true,
    RequestedBy: 862,
    Coordinator: 862,
    TaskDescription: "<div><br></div>",
  });
}

