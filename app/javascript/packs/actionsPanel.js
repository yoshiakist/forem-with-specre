// @specre 01KJ16Z3Y34HEH2GSWHHXW3NAM
const loadActionsPanel = async () => {
  const { initializeActionsPanel } = await import(
    '../actionsPanel/actionsPanel'
  );

  initializeActionsPanel();
};

loadActionsPanel();
